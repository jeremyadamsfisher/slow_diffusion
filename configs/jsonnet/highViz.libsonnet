{
  highVizCallbacks: [
    {
      "class_path": "slow_diffusion.monitoring.CountDeadUnitsCallback"
    },
    {
      "class_path": "slow_diffusion.monitoring.StatsCallback",
      "init_args": {
        "mod_filter": "convs"
      }
    }
  ]
}