local main(model, data, max_epochs, callbacks) = {
  "trainer": {
    "default_root_dir": ".lightning_root_dir",
    "log_every_n_steps": 5,
    "max_epochs": max_epochs,
    "precision": "bf16-mixed",
    "logger": {
      "class_path": "lightning.pytorch.loggers.WandbLogger",
      "init_args": {
        "project": "slow_diffusion"
      }
    },
    "callbacks": [
      {
        "class_path": "slow_diffusion.ddpm.DDPMCallback"
      },
      {
        "class_path": "CustomModelCheckpoint",
        "init_args": {
          "dirpath": "gs://slow_diffusion/training_runs/fashion_mnist_n3090",
          "filename": "ckpt-{epoch:02d}-{global_step}-{test_loss}",
          "save_top_k": 1,
          "monitor": "test_loss"
        }
      },
      {
        "class_path": "slow_diffusion.monitoring.MonitorCallback",
        "init_args": {
          "gloms": {
            "lr": "trainer.optimizers.0.param_groups.0.lr"
          }
        }
      },
    ] + callbacks,
  },
  "model": model,
  "data": data
};

{
  main: main
}