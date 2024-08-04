#!/usr/bin/env bash

set -e -o pipefail

export INSTANCE_ID=$1
export CONFIG=$2

vastai execute $INSTANCE_ID "nohup python -O -m slow_diffusion.cli fit --config slow_diffusion/configs/$CONFIG.yaml &> train.log &"