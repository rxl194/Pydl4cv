#!/bin/bash

pushd .

conda_env_root="${HOME}/miniconda3/envs/dl4cv"

mkdir -p ${conda_env_root}/etc/conda/activate.d
cp conda_activate_env.sh ${conda_env_root}/etc/conda/activate.d/env_vars.sh

mkdir -p ${conda_env_root}/etc/conda/deactivate.d
cp conda_deactivate_env.sh ${conda_env_root}/etc/conda/deactivate.d/env_vars.sh
