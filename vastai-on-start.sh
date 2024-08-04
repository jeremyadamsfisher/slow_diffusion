#!/bin/env bash

set -e -o pipefail

## Set up dev environment

mkdir /slow_diffusion
echo $GOOGLE_APPLICATION_CREDENTIALS_B64 \
    | base64 --decode \
    > /slow_diffusion/service_account.json
export GOOGLE_APPLICATION_CREDENTIALS=/slow_diffusion/service_account.json
git clone https://github.com/jeremyadamsfisher/slow_diffusion.git /slow_diffusion/slow_diffusion
gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS
cd /slow_diffusion/slow_diffusion
gsutil -m cp -r gs://slow_diffusion-gpt/char_tokenized_wikipedia_gpt3 .
mv char_tokenized_wikipedia_gpt3 wikipedia_ds

## Add creds for later, if desired

echo WANDB_API_KEY=$WANDB_API_KEY >> /etc/environment
echo GOOGLE_APPLICATION_CREDENTIALS_B64=$GOOGLE_APPLICATION_CREDENTIALS_B64 >> /etc/environment
echo GOOGLE_APPLICATION_CREDENTIALS=/slow_diffusion/service_account.json >> /etc/environment
echo PYTHONPATH=$PYTHONPATH:/slow_diffusion/slow_diffusion >> /etc/environment
echo "cd /slow_diffusion/slow_diffusion" >> ~/.bashrc
echo "gcloud auth activate-service-account --key-file=$GOOGLE_APPLICATION_CREDENTIALS" >> ~/.bashrc