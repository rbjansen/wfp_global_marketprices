#!/usr/bin/env bash

# Stop on error
set -e

echo "Starting collection of WFP data."
python collect.py
echo "Extending WFP data with coords and exchange rates."
python stage.py
