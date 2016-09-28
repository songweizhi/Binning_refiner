Binning Refiner
---

+ This pipeline was developed to refine metagenomics bins by the combination of different binning programs.

+ Contact: songwz03@gmail.com

Dependencies:
---

+ [R](https://www.r-project.org)
+ [Numpy](http://www.numpy.org)
+ [Matplotlib](http://matplotlib.org)
+ [rpy2](http://rpy2.bitbucket.org)
+ [GoogleVis](https://github.com/mages/googleVis#googlevis)
+ [CheckM](http://ecogenomics.github.io/CheckM/)
+ [BioPython](https://github.com/biopython/biopython.github.io/)
+ [Blast+ 2.2.31](http://www.ncbi.nlm.nih.gov/news/06-16-2015-blast-plus-update/)


How to run it:
---

1. Binning Refiner is implemented in python3, please use python3 instead of python.

1. First, you need to define a working directory to hold all input and output files.

1. Each set of input bins should be placed in separated folder directly under the working directory. Folder names and
bin file extension within each folder also need to be specified in commands.

1. (Optional) All bins in the above folders will be used as inputs for refining. you may want to remove bins which
are highly contaminated or ultra small before the refining step (not that much necessary, as a quality control step will
be applied after refining). To do this:

    1. First, you need to run CheckM for quality assessment of input bins. CheckM_qsuber.py can help to do this all in
    one go, please refers to the script for how to use it.

    1. Then, analysis CheckM results, Bin_filter.py was writen for this. To run it, you need to specifiy the bin size
    cutoff (in bp) and contamination cutoff in its configuration part. please refers to the script for further information.

1. Running it!

        $ python3 Binning_refiner.py -h
        usage: Binning_refiner.py [-h] -wd req) -f (req) -s (req) [-blastn (opt)]
                                  [-makeblastdb (opt)] [-bin_size_curoff (opt]
        arguments:
          -h, --help            show this help message and exit
          -wd (req)             path to working directory
          -f (req)              first bin folder name
          -s (req)              second bin folder name
          -blastn (opt)         path to blastn executable
          -makeblastdb (opt)    path to makeblastdb executable
          -bin_size_curoff (opt)
                                length cutoff for refined bins, default = 524288
                                (0.5MB)



        $ python3 CheckM_qsuber.py -h
        usage: CheckM_qsuber.py [-h] -wd required) -email (required) [-nodes (opt)]
                                [-ppn (opt)] [-memory (opt)] [-walltime (opt)]
                                [-python_v (opt)] [-hmmer_v (opt)] [-pplacer_v (opt)]
                                [-prodigal_v (opt]
        arguments:
          -h, --help         show this help message and exit
          -wd (required)     path to working directory
          -email (required)  your email address
          -nodes (opt)       nodes number needed (default = 1)
          -ppn (opt)         ppn number needed (default = 12)
          -memory (opt)      memory needed (default = 120)
          -walltime (opt)    walltime needed (default = 2:59:00)
          -python_v (opt)    python version (default: python/2.7.8)
          -hmmer_v (opt)     hmmer version (default: hmmer/3.1b2)
          -pplacer_v (opt)   pplacer version (default: pplacer/1.1.alpha16)
          -prodigal_v (opt)  prodigal version (default: prodigal/2.6.3)


        $ python3 Get_statistics.py -h
        usage: Get_statistics.py [-h] -f req) -s (req) -r (req) -o (req
        arguments:
          -h, --help  show this help message and exit
          -f (req)    path to first bin folder
          -s (req)    path to second bin folder
          -r (req)    path to refined bin folder
          -o (req)    output folder

Output files:
---

1. Refined bins (from Binning_refiner.py)

1. Cross-link (shared sequences) between input bins (from Binning_refiner.py)

    ![Sankey_plot](doc/images/sankey_plot.jpg)

    Each band in the above image represents one refined bin, we will get 9 refined bins in this case:

        MetaBAT_bin2___MyCC_bin5.fasta   MetaBAT_bin1___MyCC_bin5.fasta   MetaBAT_bin6___MyCC_bin1.fasta
        MetaBAT_bin6___MyCC_bin4.fasta   MetaBAT_bin3___MyCC_bin1.fasta   MetaBAT_bin3___MyCC_bin4.fasta
        MetaBAT_bin4___MyCC_bin2.fasta   MetaBAT_bin5___MyCC_bin3.fasta   MetaBAT_bin5___MyCC_bin6.fasta

1. Statistics of input and refined bins (from Get_statistics.py)

    ![Statistics](doc/images/statistics.png)
