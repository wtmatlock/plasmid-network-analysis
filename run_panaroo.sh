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

mkdir /tmp/panaroo-tmp
dir=/tmp/panaroo-tmp/
mkdir $dir
outdir=/path/to/panaroo_output

echo "*****************************************************"
echo "Running panaroo on all .gffs"
echo "Running panaroo at: "`date`
while read f;
do
	cp /path/to/prokka_output/"$f"/"$f".gff $dir 
done < /path/to/plasmid_names_in_community.txt
cd $dir

panaroo --clean-mode moderate -i *.gff -o ./ --aligner clustal -a core --core_threshold 0.99 -t 16

echo "****************************************************"
echo "Copying files back at: "`date`
rm *.gff
mkdir $outdir
cp -r ./ $outdir
echo "Done at: "`date`

echo "****************************************************"
echo "Finished at: "`date`
echo "****************************************************"
