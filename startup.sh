#!/bin/bash
set -e

# Activate virtual environment
source /home/airflow/.venv/bin/activate

# Start Airflow in the background
airflow standalone &

# Start Jupyter Lab in the foreground
exec jupyter lab --allow-root --ip=0.0.0.0 --no-browser --IdentityProvider.token=''
