#!/usr/bin/env bash

# Stop on error
set -e

mkdir -p data
echo "Starting collection of WFP data."
python collect.py
echo "Extending WFP data with coords and exchange rates."
python prepare.py
echo "Making some maps."
python plot.py
