local main = import 'main.libsonnet';
local tinyUNet = import 'tinyUNet.libsonnet';
local highViz = import 'highviz.libsonnet';
local fashionMNIST = import 'fashionMNIST.libsonnet';

local data = {
    "class_path": "slow_diffusion.fashionmnist.FashionMNISTDataModule",
    "init_args": {
        "bs": 1024,
        "n_workers": -1
    }
};

main.main(tinyUNet, data, 25, callbacks=highViz.highVizCallbacks)