Binning Refiner
---

+ This pipeline was developed to refine metagenomics bins by the combination of multiple binning programs.

+ Contact: Weizhi Song (songwz03@gmail.com)

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

1. Binning Refiner is implemented in python3, please use python3 to run it instead of python.

1. First, you need to define a working directory to hold all input and output files, full path to this directory need
to be specified in config.txt.

1. Each set of input bins should be placed in separated folder directly under the working directory. Folder names and
bin file extension within each folder also need to be specified in config.txt.

1. (Optional) All bins in the above folders will be used as inputs for refining. you may want to remove bins which
are highly contaminated or ultra small before the refining step (not that much necessary, as a quality control step will
be applied after refining). To do this:

    1. First, you need to run CheckM for quality assessment of input bins. CheckM_qsuber.py can help to do this all in
    one go, please refers to the script for how to use it.

    1. Then, analysis CheckM results, Bin_filter.py was writen for this. To run it, you need to specifiy the bin size
    cutoff (in bp) and contamination cutoff in its configuration part. please refers to the script for further information.

1. Running it!

        # 1. get refined bins
        $ python3 Binning_refiner.py
        # 2. quality assessment of refined bin
        $ python3 CheckM_qsubder.py
        # 3. quality summary of input/output bins (completeness, contamination, bin size, bin number, total length)
        $ python3 Get_statistics.py

Output files:
---

1. Refined bins (from Binning_refiner.py)

1. Cross-link between input bins (from Binning_refiner.py)

    ![Sankey_plot](doc/images/sankey_plot.jpg)

    Each band in the above image represents one refined bin, we will get 9 refined bins in this case:

        1. MetaBAT_bin3___MyCC_bin1.fasta   2. MetaBAT_bin1___MyCC_bin1.fasta   3. MetaBAT_bin2___MyCC_bin2.fasta
        4. MetaBAT_bin4___MyCC_bin4.fasta   5. MetaBAT_bin4___MyCC_bin7.fasta   6. MetaBAT_bin6___MyCC_bin4.fasta
        7. MetaBAT_bin6___MyCC_bin6.fasta   8. MetaBAT_bin5___MyCC_bin3.fasta   9. MetaBAT_bin5___MyCC_bin5.fasta

1. Statistics of input and refined bins (from Get_statistics.py)

    ![Statistics](doc/images/statistics.png)



