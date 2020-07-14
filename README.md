# Plasmid Network Analysis

The following outlines the analysis pipeline for...

Relevant data is available on figshare:
- Plasmid fastas: https://figshare.com/articles/dataset/incf_plasmids_fa/12652196
- Plasmid metadata:
- MASH output: https://figshare.com/articles/dataset/plasmid_MASH_csv/12652313

**Sequence Distances**
-

Plasmid sequence distances are calculated using MASH (https://github.com/marbl/Mash). We used the following command:
```
mash triangle -E -s 5000 -k 13 /path/to/fasta.fa > /path/to/edgelist.csv
```
This outputs an edge list readable by the Python module NetworkX (https://github.com/networkx/networkx), which can then be written as a weighted network in .gml format. The ```-E``` flag specifies the edge list format. A sketch length (```-s```) of 5000, and _k_-mer length (```-k```) of 13 are also specified.

**Network Thresholding**
-

Multiple heuristics are used for thresholding the network. For diagnosing the Louvain algorithmn performance over varying thresholds, the **louvain_performance.py** script for community coverage and community number is included. Also included is the **lcc_ncc.py** script for calculating the largest connected component/number of connected components. The only dependences are as follows:
- Counter from collections (https://docs.python.org/3/library/collections.html)
- python-louvain (https://github.com/taynaud/python-louvain, imported as ```community```)
- NetworkX (https://github.com/networkx/networkx)
- NumPy (https://github.com/numpy/numpy)
- pandas (https://github.com/pandas-dev/pandas)

**Community Metadata Analysis**
-

We used ```metrics.homogeneity_score``` and ```metrics.completeness_score``` from the Python module scikit-learn (https://github.com/scikit-learn/scikit-learn) to compare the community labels and metadata labels. Included is the **permutation_test.py** script for computing the permtuation test *p*-value. This script uses the random Python module (https://docs.python.org/3/library/random.html).

**Community Pangenomes**
-

We first used Prokka (https://github.com/tseemann/prokka) to annotate the plasmids. The included **run_prokka.sh** script uses the command
```
prokka /path/to/"$sample".fasta --quiet --outdir /path/to/prokka_output/"$sample" --force --prefix $sample
```
The ```--quiet``` flag suppresses the screen output, ```--outdir``` specifies the path to the output folder, ```--force``` overwrites any existsing output folder and ```--prefix``` names the output files. The GFF3 annotation output from Prokka was passed to Panaroo (https://github.com/gtonkinhill/panaroo) using the included **run_panaroo.sh** script. It uses the command
```
panaroo --clean-mode moderate -i *.gff -o ./ --aligner clustal -a core --core_threshold 0.99 -t 16
```
The ```--clean-mode``` flag determines the running mode, which we set to moderate. The path to the input is flagged by ```-i```, and the path to the output by ```-o```. We specified Clustal Omega (http://www.clustal.org/omega/) for aligning the core genes with ```--aligner```, which needs to be installed seperately. The ```-a``` flag specifies we only want to align the core genes, and ```--core_threshold``` specifies the core gene presence threshold at 99%. Finally, ```-t``` specifies the number of threads as 16.

Specifically annotating for AMR genes used Abricate (https://github.com/tseemann/abricate) with the NCBI 'Bacterial Antimicrobial Resistance Rerefence Gene' database (https://www.ncbi.nlm.nih.gov/bioproject/PRJNA313047).

**Core Gene Phylogeny**
-

For the core gene phylogeny, we used ggtree (https://github.com/YuLab-SMU/ggtree) in R to read the ```core_gene_alignment.aln``` output from Panaroo and write a neighbour-joining tree in Newick format. This was used by ClonalFrameML (https://github.com/xavierdidelot/ClonalFrameML) to produce a further tree, accounting for homologous recombination. The accompanying heatmap used the ```gene_presence_absence.Rtab``` Panaroo output.

**Other Analysis**
-
Plasmid mobility typing used MOB-typer from the MOB-suite (https://github.com/phac-nml/mob-suite). For network visualisation, we used Cytoscape (https://github.com/cytoscape/cytoscape). The software can also be used for calculating network descriptive statistics.
