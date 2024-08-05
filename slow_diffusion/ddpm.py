# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/05_ddpm.ipynb.

# %% auto 0
__all__ = ['denoisify', 'ddpm', 'DDPMCallback', 'TinyFashionMNISTDataModule']

# %% ../nbs/05_ddpm.ipynb 2
import math

import lightning as L
import torch
import torchvision
from lightning.pytorch.loggers import WandbLogger
from torch import tensor
from tqdm import tqdm

import wandb
from .data import noisify, show_images, ᾱ
from .fashionmnist import FashionMNISTDataModule
from .training import UnetLightning

# %% ../nbs/05_ddpm.ipynb 3
def denoisify(x_t, noise, t):
    return (x_t - (1 - ᾱ(t)).sqrt() * noise) / ᾱ(t).sqrt()

# %% ../nbs/05_ddpm.ipynb 4
@torch.no_grad()
def ddpm(model, sz, n_steps, device=None):
    x_t = torch.randn(sz)
    ts = torch.linspace(1 - (1 / n_steps), 0, n_steps)
    bs, *_ = x_t.shape
    if device:
        x_t = x_t.to(device)
        ts = ts.to(device)
    for t, t_next in tqdm(zip(ts, ts[1:]), unit="time step", total=n_steps - 1):
        t = t.repeat(bs)
        t_next = t_next.repeat(bs)
        noise_pred = model(x_t, t)
        x_0_pred = denoisify(x_t, noise_pred, t)
        (prev_sample, _), _ = noisify(x_0_pred, t_next)
        x_t = prev_sample

    t = tensor(0.0, device=device).repeat(bs)
    x_0 = denoisify(x_t, model(x_t, t), t)

    return x_0

# %% ../nbs/05_ddpm.ipynb 7
class DDPMCallback(L.Callback):
    def __init__(self, n_imgs=4, n_steps=100):
        super().__init__()
        self.n_imgs = n_imgs
        self.n_steps = n_steps

    def on_train_epoch_end(self, trainer, pl_module):
        sz = (
            self.n_imgs,
            pl_module.hparams.color_channels,
            *trainer.datamodule.img_size,
        )
        x_0 = (
            ddpm(pl_module.unet, sz, self.n_steps, device=pl_module.device)
            .cpu()
            .numpy()
        )
        wandb.log({"samples": show_images(x_0)})

# %% ../nbs/05_ddpm.ipynb 8
class TinyFashionMNISTDataModule(FashionMNISTDataModule):
    def post_process(self, ds):
        return ds["train"].select(range(100)).train_test_split(test_size=0.5)