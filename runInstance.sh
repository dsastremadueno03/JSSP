#!/bin/bash
#$ -S /bin/bash

# Store the instance label
INSTANCE=$1

python3 $HOME/PythonVersion/app.py "$INSTANCE"
