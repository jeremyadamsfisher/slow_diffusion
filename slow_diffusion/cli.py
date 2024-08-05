from lightning.pytorch.cli import LightningCLI
from slow_diffusion.training import UnetLightning

def cli_main():
    _ = LightningCLI(UnetLightning, save_config_kwargs={"overwrite": True})

if __name__ == "__main__":
    cli_main()