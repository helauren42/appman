#!/bin/bash

source ../venv/bin/activate
pip install -r ../requirements.txt
python3 /home/$USER/.local/appman/backend/api.py
