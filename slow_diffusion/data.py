# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_data.ipynb.

# %% auto 0
__all__ = ['ᾱ', 'noisify', 'DiffusionDataModule']

# %% ../nbs/02_data.ipynb 2
import itertools
import math
import multiprocessing
import tempfile
from pathlib import Path

import lightning as L
import matplotlib.pyplot as plt
import torch
import torchvision.transforms.functional as F
from datasets import load_dataset, load_from_disk
from einops import rearrange
from torch.utils.data import DataLoader

# %% ../nbs/02_data.ipynb 3
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
    return fig

# %% ../nbs/02_data.ipynb 5
def ᾱ(t, reshape=True):
    assert (0 <= t).all() and (t <= 1).all()
    ᾱ_ = ((t * math.pi / 2).cos() ** 2).clamp(0.0, 0.999)
    if reshape:
        ᾱ_ = ᾱ_.reshape(-1, 1, 1, 1)
    return ᾱ_

# %% ../nbs/02_data.ipynb 6
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

# %% ../nbs/02_data.ipynb 7
class DiffusionDataModule(L.LightningDataModule):
    """Lightning DataModule wrapper for huggingface datasets. Helps with
    pre-processing the image data. Just add a noisify_fn(batch)!"""

    def __init__(
        self,
        hf_ds_uri,
        bs,
        n_workers=0,
        img_size: tuple[int, int] | None = None,
        data_dir="./data",
    ):
        super().__init__()
        self.bs = bs
        self.hf_ds_uri = hf_ds_uri
        self.img_size = img_size
        self._n_workers = n_workers
        self.data_dir = Path(data_dir)

    def noisify_fn(self, x_0):
        raise NotImplementedError

    def post_process(self, ds):
        """Optional post-processing pass after download but before freezing"""
        raise NotImplementedError

    def to_tensor(self, img):
        if self.img_size is not None:
            img = img.resize(self.img_size)
        x = F.pil_to_tensor(img)
        _, h, w = x.shape
        assert h & (h - 1) == 0, f"height ({h}) must be a power of two"
        assert w & (w - 1) == 0, f"width ({w}) must be a power of two"
        return x

    def _collate(self, batch):
        x_0 = torch.stack([self.to_tensor(row["image"]) for row in batch])
        return self.noisify_fn(x_0)

    def _freeze(self, batch):
        x_0 = torch.stack([self.to_tensor(img) for img in batch["image"]])
        ((x_t, t), epsilon) = self.noisify_fn(x_0)
        return {"x_t": x_t, "t": t, "epsilon": epsilon}

    def _frozen_collate(self, rows):
        def s(feature):
            return torch.tensor([row[feature] for row in rows])

        return (s("x_t"), s("t")), s("epsilon")

    @property
    def cached_dir(self):
        return self.data_dir / f"{self.__class__.__name__}_{self.hf_ds_uri}"

    def clean(self):
        self.cached_dir.unlink()

    def setup(self, stage: str | None = None, test_splits=("test",)):
        if not self.cached_dir.exists():
            ds = load_dataset(self.hf_ds_uri)

            try:
                ds = self.post_process(ds)
            except NotImplementedError:
                pass

            for split in test_splits:
                ds[split] = ds[split].map(
                    self._freeze,
                    batched=True,
                    # We can discard the original data, as we only care about the noised information
                    remove_columns=ds[split].features.keys(),
                )

            ds.save_to_disk(self.cached_dir)

        # Load from disk to take advantage of mmapping
        self.ds = load_from_disk(self.cached_dir)

    @property
    def n_workers(self):
        if self._n_workers == -1:
            return multiprocessing.cpu_count() - 1
        else:
            return self._n_workers

    def train_dataloader(self):
        return DataLoader(
            self.ds["train"],
            shuffle=True,
            batch_size=self.bs,
            collate_fn=self._collate,
            num_workers=self.n_workers,
        )

    def val_dataloader(self):
        return DataLoader(
            self.ds["test"],
            batch_size=self.bs,
            collate_fn=self._frozen_collate,
            num_workers=self.n_workers,
        )
