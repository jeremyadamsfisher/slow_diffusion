# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_model.ipynb.

# %% auto 0
__all__ = ['InFeatureMapTensor', 'OutFeatureMapTensor', 'TimeStepTensor', 'TimeStepEmbeddingTensor', 'KaimingInitializable',
           'ConvBlock', 'timestep_embedding', 'TimeEmbeddingMixer', 'ResBlock', 'Downblock', 'Upblock',
           'TimeEmbeddingMLP', 'Unet']

# %% ../nbs/01_model.ipynb 3
import math
from typing import Sequence, TypeAlias

import matplotlib.pyplot as plt
import numpy as np
import torch
from beartype import beartype
from jaxtyping import Float, Int, jaxtyped
from torch import Tensor, nn

# %% ../nbs/01_model.ipynb 5
InFeatureMapTensor: TypeAlias = Float[Tensor, "bs c_in h_in w_in"]
OutFeatureMapTensor: TypeAlias = Float[Tensor, "bs c_out h_out w_out"]
TimeStepTensor: TypeAlias = Float[Tensor, "bs"]  # from 0 to 1
TimeStepEmbeddingTensor: TypeAlias = Float[Tensor, "bs t"]

# %% ../nbs/01_model.ipynb 7
class KaimingInitializable:
    """Helper mixin to facilitate initialization"""

    @staticmethod
    def apply_kaiming(module: torch.nn.Module) -> None:
        """Apply the module's custom kaiming initialization"""
        try:
            module._kaiming()
        except AttributeError:
            pass

    @classmethod
    def kaiming(cls, *args, **kwargs):
        model = cls(*args, **kwargs)
        model.apply(cls.apply_kaiming)
        return model

# %% ../nbs/01_model.ipynb 9
class ConvBlock(nn.Module, KaimingInitializable):
    """Wrapper for a Conv block with normalization and activation"""

    def __init__(self, c_in: int, c_out: int, ks: int = 3, stride: int = 1):
        super().__init__()
        self.ks = ks
        self.norm = nn.BatchNorm2d(c_in)
        self.act = nn.ReLU()  # 👈 SwiGLU?
        self.conv = nn.Conv2d(
            c_in,
            c_out,
            stride=stride,
            kernel_size=ks,
            padding=ks // 2,
            bias=False,
        )

    @jaxtyped(typechecker=beartype)
    def forward(self, x: InFeatureMapTensor) -> OutFeatureMapTensor:
        x = self.norm(x)
        x = self.act(x)
        x = self.conv(x)
        return x

    def _kaiming(self):
        if isinstance(self.act, (nn.ReLU,)):
            torch.nn.init.kaiming_normal_(self.conv.weight, a=0.0)
        else:
            raise ValueError
        if self.conv.bias is not None:
            torch.nn.init.constant_(self.conv.bias, 0)

# %% ../nbs/01_model.ipynb 14
@jaxtyped(typechecker=beartype)
def timestep_embedding(
    ts: TimeStepTensor, emb_dim: int, max_period: int = 10_000
) -> TimeStepEmbeddingTensor:
    exponent = -math.log(max_period) * torch.linspace(
        0, 1, emb_dim // 2, device=ts.device
    )
    embedding = ts[:, None].float() * exponent.exp()[None, :]
    embedding = torch.cat([embedding.sin(), embedding.cos()], dim=-1)
    return embedding

# %% ../nbs/01_model.ipynb 15
class TimeEmbeddingMixer(nn.Module, KaimingInitializable):
    """Incorporate the time embedding into the ResBlock logits"""

    def __init__(self, c_time, c_out):
        super().__init__()
        self.lin = nn.Linear(c_time, c_out * 2)
        self.act = nn.ReLU()  # 👈 SwiGLU?

    @jaxtyped(typechecker=beartype)
    def forward(
        self, x: InFeatureMapTensor, t_emb: TimeStepEmbeddingTensor
    ) -> OutFeatureMapTensor:
        t_emb = self.lin(self.act(t_emb))[:, :, None, None]
        scale, shift = torch.chunk(t_emb, 2, dim=1)
        return x * (1 + scale) + shift

# %% ../nbs/01_model.ipynb 17
class ResBlock(
    nn.Module,
    KaimingInitializable,
):
    """Conv resblock with the preactivation configuration and time embedding modulation"""

    def __init__(
        self, c_time: int, c_in: int, c_out: int, ks: int = 3, stride: int = 2
    ):
        super().__init__()
        self.c_time = c_time
        self.c_in = c_in
        self.c_out = c_out

        self.time_mixer = TimeEmbeddingMixer(c_time, c_out)
        self.conv_a = ConvBlock(c_in, c_out)
        self.conv_b = ConvBlock(c_out, c_out)
        if c_in != c_out:
            self.id_conv = nn.Conv2d(c_in, c_out, kernel_size=1)
        else:
            self.id_conv = None

        self.output = None

    def non_residual(self, x, t_emb):
        x = self.conv_a(x)
        x = self.time_mixer(x, t_emb)
        x = self.conv_b(x)
        return x

    def residual(self, x):
        if self.id_conv is not None:
            return self.id_conv(x)
        else:
            return x

    @jaxtyped(typechecker=beartype)
    def forward(
        self, x: InFeatureMapTensor, t_emb: TimeStepEmbeddingTensor
    ) -> OutFeatureMapTensor:
        x = self.non_residual(x, t_emb) + self.residual(x)
        self.output = x
        return x

# %% ../nbs/01_model.ipynb 21
class Downblock(nn.Module):
    """A superblock consisting of many downblocks of similar resolutions"""

    def __init__(self, c_time, c_in, c_out, downsample=True, n_layers=1):
        super().__init__()
        self.c_time = c_time
        self.c_in = c_in
        self.c_out = c_out
        self.downsample = downsample
        self.n_layers = n_layers

        self.convs = nn.ModuleList()
        self.convs.append(ResBlock(c_time, c_in, c_out, stride=1))
        for _ in range(n_layers - 1):
            self.convs.append(ResBlock(c_time, c_out, c_out, stride=1))
        self.downsampler = nn.Conv2d(c_out, c_out, kernel_size=3, stride=2, padding=1)

    @jaxtyped(typechecker=beartype)
    def forward(
        self, x: InFeatureMapTensor, t: TimeStepEmbeddingTensor
    ) -> OutFeatureMapTensor:
        for conv in self.convs:
            x = conv(x, t)
        if self.downsample:
            x = self.downsampler(x)
        return x

# %% ../nbs/01_model.ipynb 23
class Upblock(nn.Module):
    """A superblock consisting of many upblocks of similar resolutions
    and logic to use the activations of the counterpart downblock."""

    def __init__(self, c_time, c_in, c_out, upsample=True, n_layers=1):
        super().__init__()
        self.c_time = c_time
        self.c_in = c_in
        self.c_out = c_out
        self.upsample = upsample
        self.n_layers = n_layers

        self.upsampler = nn.Sequential(
            nn.Upsample(scale_factor=2),
            nn.Conv2d(c_in, c_in, kernel_size=3, padding=1),
        )
        self.convs = nn.ModuleList()
        for _ in range(n_layers - 1):
            self.convs.append(ResBlock(c_time, c_in * 2, c_in, stride=1))
        self.convs.append(ResBlock(c_time, c_in * 2, c_out, stride=1))

    @classmethod
    def from_downblock(cls, downblock):
        return cls(
            c_time=downblock.c_time,
            c_in=downblock.c_out,
            c_out=downblock.c_in,
            upsample=downblock.downsample,
            n_layers=downblock.n_layers,
        )

    @jaxtyped(typechecker=beartype)
    def forward(
        self, x: InFeatureMapTensor, downblock: Downblock, t: TimeStepEmbeddingTensor
    ) -> OutFeatureMapTensor:
        if self.upsample:
            x = self.upsampler(x)
        for up, down in zip(self.convs, reversed(downblock.convs)):
            x = up(torch.cat((x, down.output), dim=1), t)
        return x

# %% ../nbs/01_model.ipynb 25
class TimeEmbeddingMLP(nn.Module):
    """Small neural network to modify the "raw" time embeddings"""

    def __init__(self, c_in: int, c_out: int):
        super().__init__()
        self.c_in = c_in
        self.c_out = c_out
        self.time_emb_mlp = nn.Sequential(
            nn.BatchNorm1d(c_in),
            nn.Linear(c_in, c_out),
            nn.ReLU(),
            nn.Linear(c_out, c_out),
        )

    @jaxtyped(typechecker=beartype)
    def forward(self, t: TimeStepTensor) -> TimeStepEmbeddingTensor:
        # Look up the sin/cos embedding  of the time step
        x = timestep_embedding(t, self.c_in).to(t.device)
        # Allow the model to slightly modify the embeddings
        x = self.time_emb_mlp(x)
        return x

# %% ../nbs/01_model.ipynb 26
class Unet(nn.Module, KaimingInitializable):
    """Diffusion U-net with a diffusion time dimension"""

    def __init__(
        self,
        nfs: Sequence[int],
        n_blocks: Sequence[int],
        color_channels: int = 3,
    ):
        assert len(n_blocks) - 1 == len(nfs)
        super().__init__()

        self.time_embedding = TimeEmbeddingMLP(nfs[0], 4 * nfs[0])
        c_time = self.time_embedding.c_out

        # Since we use pre-activation ResBlocks, we need to use a Conv2d here
        # to avoid discarding pixel information
        self.start = nn.Conv2d(
            color_channels, nfs[0], kernel_size=(3, 3), stride=(1, 1), padding=(1, 1)
        )
        self.downblocks = nn.ModuleList()
        self.upblocks = nn.ModuleList()
        for c_in, c_out, n_layers in zip(nfs, nfs[1:], n_blocks):
            db = Downblock(
                c_time,
                c_in,
                c_out,
                n_layers=n_layers,
            )
            self.downblocks.append(db)
            self.upblocks.insert(0, Upblock.from_downblock(db))
        self.middle = ResBlock(c_time, nfs[-1], nfs[-1], stride=1)
        self.end = ConvBlock(nfs[0], color_channels)

    # Uniquely for a U-net module output dimensions must match the input dimensions
    @jaxtyped(typechecker=beartype)
    def forward(self, x_t: InFeatureMapTensor, t: TimeStepTensor) -> InFeatureMapTensor:
        te = self.time_embedding(t)
        _, c, _, _ = x_t.shape
        assert (
            c == self.start.in_channels
        ), "model color channels must match input data channels"
        x = self.start(x_t)
        for db in self.downblocks:
            x = db(x, te)
        x = self.middle(x, te)
        for ub, db in zip(self.upblocks, reversed(self.downblocks)):
            x = ub(x, db, te)
        return self.end(x)
