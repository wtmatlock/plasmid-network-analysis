#!/bin/bash

# cluster commands here

echo "****************************************************"
echo "SGE job ID: "$JOBID
echo "SGE task ID: "$SGE_TASK_ID
echo "Run on host: "`hostname`
echo "Operating system: "`uname -s`
echo "Username: "`whoami`
echo "Started at: "`date`
echo "****************************************************"

sample=$(sed -n "$SGE_TASK_ID"p /path/to/plasmid_names.txt) 
prokka=/path/to/prokka

echo "*****************************************************"
echo "Annotating assembly with Prokka."
echo "Running Prokka at: "`date`
$prokka /path/to/"$sample".fasta --quiet \
 --outdir /path/to/prokka_output/"$sample" --force \
 --prefix $sample
echo "Finished at: "`date`
echo "*****************************************************"

echo "Finished at: "`date`
