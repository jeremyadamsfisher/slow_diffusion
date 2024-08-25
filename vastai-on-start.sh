#!/bin/env bash

set -xo pipefail

## Set up dev environment

echo "deb [signed-by=/usr/share/keyrings/cloud.google.asc] http://packages.cloud.google.com/apt cloud-sdk main" \
| tee -a /etc/apt/sources.list.d/google-cloud-sdk.list \
&& curl https://packages.cloud.google.com/apt/doc/apt-key.gpg \
| tee /usr/share/keyrings/cloud.google.asc \
&& apt-get update -y \
&& apt-get install google-cloud-sdk -y

mkdir /slow_diffusion
echo $GOOGLE_APPLICATION_CREDENTIALS_B64 \
    | base64 --decode \
    > /slow_diffusion/service_account.json
export GOOGLE_APPLICATION_CREDENTIALS=/slow_diffusion/service_account.json
git clone https://github.com/jeremyadamsfisher/slow_diffusion.git /slow_diffusion/slow_diffusion
gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
cd /slow_diffusion/slow_diffusion

## Add creds for later, if desired
echo WANDB_API_KEY=$WANDB_API_KEY >> /etc/environment
echo GOOGLE_APPLICATION_CREDENTIALS_B64=$GOOGLE_APPLICATION_CREDENTIALS_B64 >> /etc/environment
echo GOOGLE_APPLICATION_CREDENTIALS=/slow_diffusion/service_account.json >> /etc/environment
echo PYTHONPATH=$PYTHONPATH:/slow_diffusion/slow_diffusion >> /etc/environment
echo "cd /slow_diffusion/slow_diffusion" >> ~/.bashrc
echo "gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS" >> ~/.bashrc