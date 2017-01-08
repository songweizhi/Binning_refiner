Binning_refiner
---

+ Binning_refiner: Improving genome bins through the combination of different binning programs
+ A manuscript describing how it works and its performance on mock and real metagenomic datasets can be found at doc/manual.
+ Version: 2.0.0
+ Last update: 2017-01-08
+ Contact: Weizhi Song (songwz03@gmail.com), Torsten Thomas(t.thomas@unsw.edu.au)
+ Affiliation: The Centre for Marine Bio-Innovation (CMB), The University of New South Wales, Sydney, Australia

Dependencies:
---

+ [R](https://www.r-project.org)
+ R package: [GoogleVis](https://github.com/mages/googleVis#googlevis)
+ Python module: [rpy2](http://rpy2.bitbucket.org)
+ Python module: [Numpy](http://www.numpy.org)
+ Python module: [Matplotlib](http://matplotlib.org)
+ Python module: [BioPython](https://github.com/biopython/biopython.github.io/)
+ [CheckM](http://ecogenomics.github.io/CheckM/)

How to run:
---

1. Binning_refiner takes two or three binning programs produced bin sets as inputs. You need to define a working directory to
hold all input and output files. Input bin sets from different binning programs need to be placed in different folders
directly under working directory.

1. Accepted bin file extensions include 'fa', 'fas' or 'fasta'. All input bins in the same folder must have the same extension.

1. Binning_refiner scripts are implemented in python3, please use python3 instead of python.

1. For Katana users from UNSW, a specialized manual was prepared and placed at doc/manual.


        # For help:
        python3 Binning_refiner.py -h
        python3 CheckM_runner.py -h
        python3 Get_statistics.py -h

        # Example commands:
        # 1. get refined bins
        python3 Binning_refiner.py -1 MetaBAT -2 MyCC
        python3 Binning_refiner.py -1 MetaBAT -2 MyCC -3 Concoct

        # 2. get qualities for each of the three bin sets
        python3 CheckM_runner.py -1 MetaBAT -2 MyCC -r outputs/Refined -pbs -qsub
        python3 CheckM_runner.py -1 MetaBAT -2 MyCC -3 Concoct -r outputs/Refined -pbs -qsub

        # 3. get statistics
        python3 Get_statistics.py -1 MetaBAT -2 MyCC -r outputs/Refined
        python3 Get_statistics.py -1 MetaBAT -2 MyCC -3 Concoct -r outputs/Refined


Output files:
---

1. All refined bins larger than defined size cutoff

1. Refined contamination-free bins (you can customize the completeness cutoff for contamination-free bins with argument "-contamination_free_bin_completeness_cutoff" from Get_statistics.py)

1. Refined good bins (you can customize the completeness and contamination cutoff for good bins with argument "-good_bin_completeness_cutoff" and "-good_bin_completeness_cutoff" from Get_statistics.py)

1. Cross-link (shared sequences) between input bins. Each band will be treated as a refined bin, the width is proportional to its size. We will get 9 refined bins in the illustration.

    ![Sankey_plot](doc/images/sankey_plot.jpg)

1. Statistics of input and refined bins

    ![Statistics](doc/images/statistics.png)
