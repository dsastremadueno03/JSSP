#!/bin/bash
#$ -S /bin/bash

for i in $(seq 1 1 61); do
	qsub -q all.q@slave1.iscop oneInstance.sh "$i" 0
done
wait # Wait for all background processes to finish
