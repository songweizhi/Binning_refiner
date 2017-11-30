Binning_refiner
---

Publication
---
+ Song WZ, Thomas T (2017) Binning_refiner: Improving genome bins through the combination of different binning programs. Bioinformatics, 33(12), 1873-1875. http://dx.doi.org/10.1093/bioinformatics/btx086
+ Contact: Weizhi Song (songwz03@gmail.com), Torsten Thomas(t.thomas@unsw.edu.au)
+ Affiliation: The Centre for Marine Bio-Innovation (CMB), The University of New South Wales, Sydney, Australia

Dependencies:
---

+ [BioPython](https://github.com/biopython/biopython.github.io/)

Change Log:
---
Version 1.2 (2017-11-30):
+  Binning_refiner was simplified to keep only the core functions, which made it much easier to install and use, hope you enjoy it :)



How to install:
---

The only thing you need to do is to install the latest version of Python3 and Biopython.


How to run:
---

1. Binning_refiner takes two or three binning programs produced bin sets as inputs. You need to define a working directory to
hold all input and output files. Input bin sets from different binning programs need to be placed in different folders
directly under working directory.

1. Accepted bin file extensions include 'fa', 'fas' or 'fasta'. All input bins in the same folder must have the same extension.

1. Binning_refiner scripts are implemented in python3, please use python3 instead of python.

        # For two binning programs (e.g. MetaBAT and MyCC)
        python3 Binning_refiner.py -1 MetaBAT_bins -2 MyCC_bins

        # For two binning programs (e.g. MetaBAT, MyCC and CONCOCT)
        python3 Binning_refiner.py -1 MetaBAT_bins -2 MyCC_bins -3 CONCOCT_bins

Output files:
---

1. All refined bins larger than defined bin size cutoff.
1. The id of the contigs in the refined bins.
1. The size of refined bins and where its contigs come from.

