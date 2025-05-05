#!/bin/bash
#$ -S /bin/bash

# The script will run 12 instances of the Python script in parallel, each with a different argument
for i in $(seq 5 5 61); do
    python3 $HOME/PythonVersion/app.py "$i" & # Run the script in the background
done

wait # Wait for all background processes to finish
