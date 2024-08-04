# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/02_training.ipynb.

# %% auto 0
__all__ = ['CLIMixin', 'UnetLightning']

# %% ../nbs/02_training.ipynb 2
import ast
from typing import Sequence

import lightning as L
import torch
from beartype import beartype
from pydantic import BaseModel

from .model import Unet

# %% ../nbs/02_training.ipynb 3
class CLIMixin:
    """CLI parser"""

    @staticmethod
    def add_model_specific_args(parent_parser):
        parser = parent_parser.add_argument_group("Unet")

        # model config
        parser.add_argument("--nfs", type=ast.literal_eval)
        parser.add_argument("--n_blocks", type=ast.literal_eval)
        parser.add_argument("--color_channels", type=int)

        # training config
        parser.add_argument("--lr", type=float, default=4e-3)
        parser.add_argument("--one_cycle_pct_start", type=float, default=0.3)
        parser.add_argument("--one_cycle_div_factor", type=float, default=25)
        parser.add_argument("--one_cycle_final_div_factor", type=float, default=1e4)
        parser.add_argument("--adamw_epsilon", type=float, default=1e-5)

        return parent_parser

# %% ../nbs/02_training.ipynb 4
class UnetLightning(L.LightningModule, CLIMixin):
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
            adamw_epsilon:  term added to the denominator to improve numerical
                stability. PyTorch defaults to 1e-8. 1e-5 is better.
        """
        super().__init__()
        self.unet = Unet(nfs=nfs, n_blocks=n_blocks, color_channels=color_channels)
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
