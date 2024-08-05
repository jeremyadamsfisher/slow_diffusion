# Autogenerated by nbdev

d = { 'settings': { 'branch': 'main',
                'doc_baseurl': '/slow_diffusion',
                'doc_host': 'https://jeremyadamsfisher.github.io',
                'git_url': 'https://github.com/jeremyadamsfisher/slow_diffusion',
                'lib_path': 'slow_diffusion'},
  'syms': { 'slow_diffusion.cli': {},
            'slow_diffusion.core': {'slow_diffusion.core.foo': ('core.html#foo', 'slow_diffusion/core.py')},
            'slow_diffusion.data': { 'slow_diffusion.data.DiffusionDataModule': ('data.html#diffusiondatamodule', 'slow_diffusion/data.py'),
                                     'slow_diffusion.data.DiffusionDataModule.__init__': ( 'data.html#diffusiondatamodule.__init__',
                                                                                           'slow_diffusion/data.py'),
                                     'slow_diffusion.data.DiffusionDataModule._collate': ( 'data.html#diffusiondatamodule._collate',
                                                                                           'slow_diffusion/data.py'),
                                     'slow_diffusion.data.DiffusionDataModule._freeze': ( 'data.html#diffusiondatamodule._freeze',
                                                                                          'slow_diffusion/data.py'),
                                     'slow_diffusion.data.DiffusionDataModule._frozen_collate': ( 'data.html#diffusiondatamodule._frozen_collate',
                                                                                                  'slow_diffusion/data.py'),
                                     'slow_diffusion.data.DiffusionDataModule.cached_dir': ( 'data.html#diffusiondatamodule.cached_dir',
                                                                                             'slow_diffusion/data.py'),
                                     'slow_diffusion.data.DiffusionDataModule.clean': ( 'data.html#diffusiondatamodule.clean',
                                                                                        'slow_diffusion/data.py'),
                                     'slow_diffusion.data.DiffusionDataModule.n_workers': ( 'data.html#diffusiondatamodule.n_workers',
                                                                                            'slow_diffusion/data.py'),
                                     'slow_diffusion.data.DiffusionDataModule.noisify_fn': ( 'data.html#diffusiondatamodule.noisify_fn',
                                                                                             'slow_diffusion/data.py'),
                                     'slow_diffusion.data.DiffusionDataModule.post_process': ( 'data.html#diffusiondatamodule.post_process',
                                                                                               'slow_diffusion/data.py'),
                                     'slow_diffusion.data.DiffusionDataModule.setup': ( 'data.html#diffusiondatamodule.setup',
                                                                                        'slow_diffusion/data.py'),
                                     'slow_diffusion.data.DiffusionDataModule.to_tensor': ( 'data.html#diffusiondatamodule.to_tensor',
                                                                                            'slow_diffusion/data.py'),
                                     'slow_diffusion.data.DiffusionDataModule.train_dataloader': ( 'data.html#diffusiondatamodule.train_dataloader',
                                                                                                   'slow_diffusion/data.py'),
                                     'slow_diffusion.data.DiffusionDataModule.val_dataloader': ( 'data.html#diffusiondatamodule.val_dataloader',
                                                                                                 'slow_diffusion/data.py'),
                                     'slow_diffusion.data.noisify': ('data.html#noisify', 'slow_diffusion/data.py'),
                                     'slow_diffusion.data.show_images': ('data.html#show_images', 'slow_diffusion/data.py'),
                                     'slow_diffusion.data.ᾱ': ('data.html#ᾱ', 'slow_diffusion/data.py')},
            'slow_diffusion.ddpm': { 'slow_diffusion.ddpm.DDPMCallback': ('ddpm.html#ddpmcallback', 'slow_diffusion/ddpm.py'),
                                     'slow_diffusion.ddpm.DDPMCallback.__init__': ( 'ddpm.html#ddpmcallback.__init__',
                                                                                    'slow_diffusion/ddpm.py'),
                                     'slow_diffusion.ddpm.DDPMCallback.on_train_epoch_end': ( 'ddpm.html#ddpmcallback.on_train_epoch_end',
                                                                                              'slow_diffusion/ddpm.py'),
                                     'slow_diffusion.ddpm.TinyFashionMNISTDataModule': ( 'ddpm.html#tinyfashionmnistdatamodule',
                                                                                         'slow_diffusion/ddpm.py'),
                                     'slow_diffusion.ddpm.TinyFashionMNISTDataModule.post_process': ( 'ddpm.html#tinyfashionmnistdatamodule.post_process',
                                                                                                      'slow_diffusion/ddpm.py'),
                                     'slow_diffusion.ddpm.ddpm': ('ddpm.html#ddpm', 'slow_diffusion/ddpm.py'),
                                     'slow_diffusion.ddpm.denoisify': ('ddpm.html#denoisify', 'slow_diffusion/ddpm.py')},
            'slow_diffusion.fashionmnist': { 'slow_diffusion.fashionmnist.FashionMNISTDataModule': ( 'fashion_mnist.html#fashionmnistdatamodule',
                                                                                                     'slow_diffusion/fashionmnist.py'),
                                             'slow_diffusion.fashionmnist.FashionMNISTDataModule.__init__': ( 'fashion_mnist.html#fashionmnistdatamodule.__init__',
                                                                                                              'slow_diffusion/fashionmnist.py'),
                                             'slow_diffusion.fashionmnist.FashionMNISTDataModule.noisify_fn': ( 'fashion_mnist.html#fashionmnistdatamodule.noisify_fn',
                                                                                                                'slow_diffusion/fashionmnist.py')},
            'slow_diffusion.model': { 'slow_diffusion.model.ConvBlock': ('model.html#convblock', 'slow_diffusion/model.py'),
                                      'slow_diffusion.model.ConvBlock.__init__': ( 'model.html#convblock.__init__',
                                                                                   'slow_diffusion/model.py'),
                                      'slow_diffusion.model.ConvBlock._kaiming': ( 'model.html#convblock._kaiming',
                                                                                   'slow_diffusion/model.py'),
                                      'slow_diffusion.model.ConvBlock.forward': ('model.html#convblock.forward', 'slow_diffusion/model.py'),
                                      'slow_diffusion.model.Downblock': ('model.html#downblock', 'slow_diffusion/model.py'),
                                      'slow_diffusion.model.Downblock.__init__': ( 'model.html#downblock.__init__',
                                                                                   'slow_diffusion/model.py'),
                                      'slow_diffusion.model.Downblock.forward': ('model.html#downblock.forward', 'slow_diffusion/model.py'),
                                      'slow_diffusion.model.KaimingInitializable': ( 'model.html#kaiminginitializable',
                                                                                     'slow_diffusion/model.py'),
                                      'slow_diffusion.model.KaimingInitializable.apply_kaiming': ( 'model.html#kaiminginitializable.apply_kaiming',
                                                                                                   'slow_diffusion/model.py'),
                                      'slow_diffusion.model.KaimingInitializable.kaiming': ( 'model.html#kaiminginitializable.kaiming',
                                                                                             'slow_diffusion/model.py'),
                                      'slow_diffusion.model.ResBlock': ('model.html#resblock', 'slow_diffusion/model.py'),
                                      'slow_diffusion.model.ResBlock.__init__': ('model.html#resblock.__init__', 'slow_diffusion/model.py'),
                                      'slow_diffusion.model.ResBlock.forward': ('model.html#resblock.forward', 'slow_diffusion/model.py'),
                                      'slow_diffusion.model.ResBlock.non_residual': ( 'model.html#resblock.non_residual',
                                                                                      'slow_diffusion/model.py'),
                                      'slow_diffusion.model.ResBlock.residual': ('model.html#resblock.residual', 'slow_diffusion/model.py'),
                                      'slow_diffusion.model.TimeEmbeddingMLP': ('model.html#timeembeddingmlp', 'slow_diffusion/model.py'),
                                      'slow_diffusion.model.TimeEmbeddingMLP.__init__': ( 'model.html#timeembeddingmlp.__init__',
                                                                                          'slow_diffusion/model.py'),
                                      'slow_diffusion.model.TimeEmbeddingMLP.forward': ( 'model.html#timeembeddingmlp.forward',
                                                                                         'slow_diffusion/model.py'),
                                      'slow_diffusion.model.TimeEmbeddingMixer': ( 'model.html#timeembeddingmixer',
                                                                                   'slow_diffusion/model.py'),
                                      'slow_diffusion.model.TimeEmbeddingMixer.__init__': ( 'model.html#timeembeddingmixer.__init__',
                                                                                            'slow_diffusion/model.py'),
                                      'slow_diffusion.model.TimeEmbeddingMixer.forward': ( 'model.html#timeembeddingmixer.forward',
                                                                                           'slow_diffusion/model.py'),
                                      'slow_diffusion.model.Unet': ('model.html#unet', 'slow_diffusion/model.py'),
                                      'slow_diffusion.model.Unet.__init__': ('model.html#unet.__init__', 'slow_diffusion/model.py'),
                                      'slow_diffusion.model.Unet.forward': ('model.html#unet.forward', 'slow_diffusion/model.py'),
                                      'slow_diffusion.model.Upblock': ('model.html#upblock', 'slow_diffusion/model.py'),
                                      'slow_diffusion.model.Upblock.__init__': ('model.html#upblock.__init__', 'slow_diffusion/model.py'),
                                      'slow_diffusion.model.Upblock.forward': ('model.html#upblock.forward', 'slow_diffusion/model.py'),
                                      'slow_diffusion.model.Upblock.from_downblock': ( 'model.html#upblock.from_downblock',
                                                                                       'slow_diffusion/model.py'),
                                      'slow_diffusion.model.timestep_embedding': ( 'model.html#timestep_embedding',
                                                                                   'slow_diffusion/model.py')},
            'slow_diffusion.predict': {},
            'slow_diffusion.training': { 'slow_diffusion.training.CLIMixin': ('training.html#climixin', 'slow_diffusion/training.py'),
                                         'slow_diffusion.training.CLIMixin.add_model_specific_args': ( 'training.html#climixin.add_model_specific_args',
                                                                                                       'slow_diffusion/training.py'),
                                         'slow_diffusion.training.UnetLightning': ( 'training.html#unetlightning',
                                                                                    'slow_diffusion/training.py'),
                                         'slow_diffusion.training.UnetLightning.__init__': ( 'training.html#unetlightning.__init__',
                                                                                             'slow_diffusion/training.py'),
                                         'slow_diffusion.training.UnetLightning.configure_optimizers': ( 'training.html#unetlightning.configure_optimizers',
                                                                                                         'slow_diffusion/training.py'),
                                         'slow_diffusion.training.UnetLightning.step': ( 'training.html#unetlightning.step',
                                                                                         'slow_diffusion/training.py'),
                                         'slow_diffusion.training.UnetLightning.training_step': ( 'training.html#unetlightning.training_step',
                                                                                                  'slow_diffusion/training.py'),
                                         'slow_diffusion.training.UnetLightning.validation_step': ( 'training.html#unetlightning.validation_step',
                                                                                                    'slow_diffusion/training.py')}}}
