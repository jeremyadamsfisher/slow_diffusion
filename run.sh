#!/usr/bin/env bash

set -e -o pipefail

PYTHONPATH=. python slow_diffusion/cli.py fit --config configs/$1.yaml