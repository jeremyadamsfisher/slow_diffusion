local main = import 'main.libsonnet';
local model = import '85MUNet.libsonnet';
local highViz = import 'highViz.libsonnet';
local fashionMNIST = import 'fashionMNIST.libsonnet';

local data = {
    "class_path": "slow_diffusion.fashionmnist.FashionMNISTDataModule",
    "init_args": {
        "bs": 512,
        "n_workers": -1
    }
};

main.main(model, data, 25, callbacks=[])