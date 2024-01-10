#!/bin/bash

# Install dependent packages
pip install -r requirements.txt

# Start main.py and redirect the output to logs/logs.txt
nohup python3 main.py > logs/logs.txt 2>&1 &
