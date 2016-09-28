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

1. It is recommended to define a working directory to hold all input and output files. Input bin sets from different
binning programs need to be placed in different folders.

1. Accepted bin file extensions include 'fa', 'fas' or 'fasta'. All input bins from the same binning program must have the same extension.

1. (Reminder) As CheckM is a memory eating program, CheckM_qsuber.py will submit one job for each input/output bin. This will become annoying
if you have hundreds of bins, as the same number of emails will influx your account!

        # This pipeline is implemented in python3, please use python3 instead of python

        # Example commands:
        $ /share/apps/python/3.4.3/bin/python3 /home/z5039045/Binning_refiner/Binning_refiner.py -wd /home/testdata -f MetaBAT -s MyCC
        $ /share/apps/python/3.4.3/bin/python3 /home/z5039045/Binning_refiner/CheckM_qsuber.py -email songwz03@gmail.com -wd /home/testdata/MetaBAT
        $ /share/apps/python/3.4.3/bin/python3 /home/z5039045/Binning_refiner/Get_statistics.py -f /home/testdata/MetaBAT -s /home/testdata/MyCC -r /home/testdata/outputs/Refined -o /home/testdata

        # For help:
        $ /share/apps/python/3.4.3/bin/python3 /home/z5039045/Binning_refiner/Binning_refiner.py -h
        $ /share/apps/python/3.4.3/bin/python3 /home/z5039045/Binning_refiner/CheckM_qsuber.py -h
        $ /share/apps/python/3.4.3/bin/python3 /home/z5039045/Binning_refiner/Get_statistics.py -h


Output files:
---

1. Refined bins (from Binning_refiner.py)

1. Contamination-free refined bins (from Get_statistics.py)

1. Cross-link (shared sequences) between input bins (from Binning_refiner.py)

    ![Sankey_plot](doc/images/sankey_plot.jpg)

    Each band in the above image represents one refined bin, we will get 9 refined bins in this case:

        MetaBAT_bin2___MyCC_bin5.fasta   MetaBAT_bin1___MyCC_bin5.fasta   MetaBAT_bin6___MyCC_bin1.fasta
        MetaBAT_bin6___MyCC_bin4.fasta   MetaBAT_bin3___MyCC_bin1.fasta   MetaBAT_bin3___MyCC_bin4.fasta
        MetaBAT_bin4___MyCC_bin2.fasta   MetaBAT_bin5___MyCC_bin3.fasta   MetaBAT_bin5___MyCC_bin6.fasta

1. Statistics of input and refined bins (from Get_statistics.py)

    ![Statistics](doc/images/statistics.png)
