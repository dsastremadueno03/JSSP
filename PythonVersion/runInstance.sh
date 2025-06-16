#!/bin/bash
#$ -S /bin/bash
for j in $(seq 0 1 12); do
# The script will run 12 instances of the Python script in parallel, each with a different argument
	for i in $(seq 5 5 61); do
		qsub -q all.q@slave1.iscop oneInstance.sh "$i" "$j"
	done
done
wait # Wait for all background processes to finish
