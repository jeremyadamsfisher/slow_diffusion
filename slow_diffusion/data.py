# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/04_data.ipynb.

# %% auto 0
__all__ = ['ᾱ', 'noisify', 'DiffusionDataModule']

# %% ../nbs/04_data.ipynb 2
import itertools
import math
import multiprocessing
import tempfile
from functools import cache

import lightning as L
import matplotlib.pyplot as plt
import torch
import torchvision.transforms.functional as F
from datasets import load_dataset
from einops import rearrange
from torch.utils.data import DataLoader, Dataset, default_collate
from torchvision import transforms

# %% ../nbs/04_data.ipynb 3
def show_images(imgs, titles=[], figsize=(4, 4)):
    n, *_ = imgs.shape
    k = math.ceil(math.sqrt(n))
    imgs = rearrange(imgs, "bs c h w -> bs h w c")
    fig, axes = plt.subplots(k, k, figsize=figsize)
    for title, img, ax in itertools.zip_longest(titles, imgs, axes.flatten()):
        ax.imshow(img)
        if title:
            ax.set(title=title)
    fig.tight_layout()

# %% ../nbs/04_data.ipynb 5
def ᾱ(t, reshape=True):
    assert (0 <= t).all() and (t <= 1).all()
    ᾱ_ = ((t * math.pi / 2).cos() ** 2).clamp(0.0, 0.999)
    if reshape:
        ᾱ_ = ᾱ_.reshape(-1, 1, 1, 1)
    return ᾱ_

# %% ../nbs/04_data.ipynb 6
def noisify(x_0, t=None):
    n, *_ = x_0.shape
    device = x_0.device

    if t is None:
        t = torch.rand((n,), device=device)

    # Sample 2D noise for each example in the batch
    ε = torch.randn(x_0.shape, device=device)

    # Add noise according to the equation in Algorithm 1, such
    # that the variance of the distribution does not change. Also,
    # ensure that the overall magnitude does not change by 0-centering
    # x_0 and 0.5-centering x_t
    x_t = ᾱ(t).sqrt() * (x_0) + (1 - ᾱ(t)).sqrt() * ε

    return ((x_t, t), ε)

# %% ../nbs/04_data.ipynb 7
class DiffusionDataModule:
    def __init__(self, hf_ds_uri, noisfy_fn, bs):
        self.bs = bs
        self.noisfy_fn = noisfy_fn
        self.hf_ds_uri = hf_ds_uri

    def _collate(self, batch):
        x_0 = torch.stack([F.pil_to_tensor(row["image"]) for row in batch])
        return self.noisfy_fn(x_0)

    def _freeze(self, batch):
        x_0 = torch.stack([F.pil_to_tensor(img) for img in batch["image"]])
        ((x_t, t), epsilon) = self.noisfy_fn(x_0)
        return {"x_t": x_t, "t": t, "epsilon": epsilon}

    def _frozen_collate(self, rows):
        def s(feature):
            return torch.tensor([row[feature] for row in rows])

        return (s("x_t"), s("t")), s("epsilon")

    def setup(self, stage: str | None = None, test_splits=("test",)):
        self.ds = load_dataset(self.hf_ds_uri)
        for split in test_splits:
            self.ds[split] = self.ds[split].map(
                self._freeze,
                batched=True,
                # We can discard the original data, as we only care about the noised information
                remove_columns=self.ds[split].features.keys(),
            )

    def train_dataloader(self):
        return DataLoader(
            self.ds["train"],
            batch_size=self.bs,
            collate_fn=self._collate,
        )

    def val_dataloader(self):
        return DataLoader(
            self.ds["test"],
            batch_size=self.bs,
            collate_fn=self._frozen_collate,
        )
