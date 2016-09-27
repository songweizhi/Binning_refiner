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
        $ python3 Binning_refiner.py -wd -f -fx -s -sx -blastn -makeblastdb
        $ python3 Binning_refiner.py -wd /Users/songweizhi/Desktop/testdata -f MetaBAT -fx fa -s MyCC -sx fasta -blastn /Users/songweizhi/Softwares/ncbi-blast-2.4.0+/bin/blastn -makeblastdb /Users/songweizhi/Softwares/ncbi-blast-2.4.0+/bin/makeblastdb

        # 2. quality assessment of refined bin
        $ python3 CheckM_qsuber.py -wd -bx -email
        $ python3 CheckM_qsuber.py -wd /Users/songweizhi/Desktop/testdata/MetaBAT -bx fa -email weizhi.song@student.unsw.edu.au
        $ python3 CheckM_qsuber.py -wd /Users/songweizhi/Desktop/testdata/MyCC -bx fasta -email weizhi.song@student.unsw.edu.au
        $ python3 CheckM_qsuber.py -wd /Users/songweizhi/Desktop/testdata/Refined -bx fasta -email weizhi.song@student.unsw.edu.au

        # 3. quality summary of input/output bins (completeness, contamination, bin size, bin number, total length)
        $ python3 Get_statistics.py -f -fx -s -sx -r -rx -o
        $ python3 Get_statistics.py -f /Users/songweizhi/Desktop/testdata/MetaBAT -fx fa -s /Users/songweizhi/Desktop/testdata/MyCC -sx fasta -r /Users/songweizhi/Desktop/testdata/outputs/refined_bins -rx fasta -o /Users/songweizhi/Desktop/testdata

Output files:
---

1. Refined bins (from Binning_refiner.py)

1. Cross-link between input bins (from Binning_refiner.py)

    ![Sankey_plot](doc/images/sankey_plot.jpg)

    Each band in the above image represents one refined bin, we will get 9 refined bins in this case:

        MetaBAT_bin2___MyCC_bin5.fasta   MetaBAT_bin1___MyCC_bin5.fasta   MetaBAT_bin6___MyCC_bin1.fasta
        MetaBAT_bin6___MyCC_bin4.fasta   MetaBAT_bin3___MyCC_bin1.fasta   MetaBAT_bin3___MyCC_bin4.fasta
        MetaBAT_bin4___MyCC_bin2.fasta   MetaBAT_bin5___MyCC_bin3.fasta   MetaBAT_bin5___MyCC_bin6.fasta

1. Statistics of input and refined bins (from Get_statistics.py)

    ![Statistics](doc/images/statistics.png)
