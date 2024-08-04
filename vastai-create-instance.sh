#!/usr/bin/env bash

set -e -o pipefail

# Check if the -m flag is set
if [[ $1 == "-m" ]]; then
    INSTANCE_ID=$2
else
    echo Please find an instance to deploy to!
    exit 1
fi

vastai create instance $INSTANCE_ID \
    --image jeremyadamsfisher1123/slow-diffusion \
    --env "-e WANDB_API_KEY=$(cat .secrets.json | jq -r .WANDB_API_KEY) -e GOOGLE_APPLICATION_CREDENTIALS_B64=$(base64 < ./service_account.json)" \
    --disk 100 \
    --ssh \
    --onstart ./vastai-on-start.sh