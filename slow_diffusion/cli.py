import os
from datetime import datetime

import lightning as L
from lightning.pytorch.cli import LightningCLI

from slow_diffusion import __version__
from slow_diffusion.training import UnetLightning

class CustomModelCheckpoint(L.pytorch.callbacks.ModelCheckpoint):
    def __init__(self, dirpath, *args, **kwargs):
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
        dirpath_ = os.path.join(
            dirpath,
            __version__,
            dt_string,
        )
        super().__init__(*args, **kwargs, dirpath=dirpath_)


def cli_main():
    _ = LightningCLI(UnetLightning, save_config_kwargs={"overwrite": True})


if __name__ == "__main__":
    cli_main()
