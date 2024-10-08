# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/01_training.ipynb.

# %% auto 0
__all__ = ['UnetLightning', 'get_tiny_unet_lightning']

# %% ../nbs/01_training.ipynb 2
from typing import Callable, Sequence

import lightning as L
import torch
from beartype import beartype
from torch import nn

from .model import NonPreactResBlock, PreactResBlock, Unet

# %% ../nbs/01_training.ipynb 3
class UnetLightning(L.LightningModule):
    @beartype
    def __init__(
        self,
        nfs: Sequence[int],
        n_blocks: Sequence[int],
        color_channels: int,
        lr: float = 4e-3,
        one_cycle_pct_start: float = 0.3,
        one_cycle_div_factor: float = 25.0,
        one_cycle_final_div_factor: float = 1e4,
        adamw_epsilon: float = 1e-5,
        act: type[torch.nn.Module] | str = "torch.nn.ReLU",
        res_block_cls: type[nn.Module] | str = "PreactResBlock",
        kaiming: bool = False,
    ):
        """Unet training code

        Args:
            nfs:  Number of channels in a {Up,Down}block
            n_blocks: Number of sub-blocks in {Up,Down}block. Should have 1
                more entry than `nfs`
            color_channels: Color channels, or however many dimensions in the
                VAE bottleneck space
            lr: learning rate
            one_cycle_pct_start: The percentage of the cycle (in number of
                steps) spent increasing the learning rate. Default: 0.3
            one_cycle_div_factor:  Determines the initial learning rate
                via initial_lr = max_lr/div_factor Default: 25
            one_cycle_final_div_factor: Determines the minimum learning rate
                via min_lr = initial_lr/final_div_factor Default: 1e4
            adamw_epsilon: term added to the denominator to improve numerical
                stability. PyTorch defaults to 1e-8. 1e-5 is better.
            act: activation function
            res_block_cls: classic or preactivation resblock
            kaiming: perform kaiming initialization
        """
        super().__init__()
        if isinstance(act, str):
            act = eval(act)
        if isinstance(res_block_cls, str):
            res_block_cls = eval(res_block_cls)
        self.unet = Unet(
            nfs=nfs,
            n_blocks=n_blocks,
            color_channels=color_channels,
            act=act,
            res_block_cls=res_block_cls,
        )
        if kaiming:
            from slow_diffusion.init import kaiming as kaiming_

            self.unet.apply(kaiming_)
        self.save_hyperparameters()
        self.loss_fn = torch.nn.MSELoss()

    def step(self, batch):
        (x_t, t), epsilon = batch
        preds = self.unet(x_t, t)
        return self.loss_fn(preds, epsilon)

    def training_step(self, batch, batch_idx):
        loss = self.step(batch)
        self.log("train_loss", loss, on_step=True, sync_dist=True)
        return loss

    def validation_step(self, batch, batch_idx):
        loss = self.step(batch)
        self.log("test_loss", loss, sync_dist=True)
        return loss

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(
            self.parameters(),
            lr=self.hparams.lr,
            eps=self.hparams.adamw_epsilon,
        )
        return {
            "optimizer": optimizer,
            "lr_scheduler": {
                "scheduler": torch.optim.lr_scheduler.OneCycleLR(
                    optimizer,
                    max_lr=self.hparams.lr,
                    total_steps=self.trainer.estimated_stepping_batches,
                    pct_start=self.hparams.one_cycle_pct_start,
                    div_factor=self.hparams.one_cycle_div_factor,
                    final_div_factor=self.hparams.one_cycle_final_div_factor,
                ),
                "interval": "step",
                "frequency": 1,  # Update the LR every step
                "monitor": "test_loss",  # Not relevant for OneCycleLR but specified anyways
                "strict": True,  # FYI doesn't need to be strict because the monitor is irrelevant
            },
        }

# %% ../nbs/01_training.ipynb 5
def get_tiny_unet_lightning(**kwargs):
    if "act" not in kwargs:
        kwargs["act"] = nn.ReLU
    return UnetLightning(
        nfs=[32, 64, 128, 256, 384],
        n_blocks=[3, 2, 1, 1, 1, 1],
        color_channels=1,
        **kwargs,
    )
