local main = import 'main.libsonnet';
local tinyUNet = import 'tinyUNet.libsonnet';
local highViz = import 'highviz.libsonnet';

local model = {
  "model": {
    "nfs": [
      16,
      32,
      64
    ],
    "n_blocks": [
      1,
      1,
      1,
      1
    ],
    "color_channels": 1,
    "lr": 0.004
  }
};

local singleProcDataModule = {
    "class_path": "slow_diffusion.fashionmnist.FashionMNISTDataModule",
    "init_args": {
        "bs": 32,
        "n_workers": 0
    }
};

main.main(model, singleProcDataModule, 1, callbacks=highViz.highVizCallbacks)