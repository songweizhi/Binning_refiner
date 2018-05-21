![logo](images/logo.jpg)

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
+  Binning_refiner has been simplified to keep only the core functions, which made it much easier to install and use, hope you enjoy it :)

Important notification !!!

+  In the original version of Binning_refiner, the blast approach (as described in its [publication](http://dx.doi.org/10.1093/bioinformatics/btx086))
was used to identify the same contig among input bin sets. As Binning_refiner was designed to refine bins derived from the same set of assemblies
and the blast step is time-consuming (especially for big dataset), the same assembly among different bin sets was identified by its ID rather than
blastn, which made Binning_refiner much faster to run and more easier to install.


How to install:
---
1. Install Python and Biopython.

        # for Katana users from UNSW, simply run
        $ module load python/3.5.2

1. Download Binning_refiner.py to the place your want, it is ready to run now

        $ python path/to/Binning_refiner.py -h

1. In case you want to see the correlations between your input bin sets (figure below), you need to have R and its following three packages installed: [tools](https://www.rdocumentation.org/packages/tools),
[optparse](https://cran.r-project.org/web/packages/optparse/index.html) and [googleVis](https://cran.r-project.org/web/packages/googleVis/index.html)


Help information:
---
        python Binning_refiner.py -h
          -h, --help      show this help message and exit
          -1              first bin folder name
          -2              second bin folder name
          -3              third bin folder name
          -x1             file extension for bin set 1, default: fasta
          -x2             file extension for bin set 2, default: fasta
          -x3             file extension for bin set 3, default: fasta
          -prefix         prefix of refined bins, default: Refined
          -ms             minimal size for refined bins, default: 524288 (0.5Mbp)




How to run:
---

1. All bins in one folder must have same file extension.

1. Binning_refiner now compatible with both python2 and python3.

        # For two binning programs (e.g. MetaBAT and MyCC)
        python Binning_refiner.py -1 MetaBAT -2 MyCC -x1 fa -prefix Refined

        # For three binning programs (e.g. MetaBAT, MyCC and CONCOCT)
        python Binning_refiner.py -1 MetaBAT -2 MyCC -3 CONCOCT -x1 fa -x3 fa -prefix Refined

Output files:
---
1. All refined bins larger than defined bin size cutoff.
1. The id of the contigs in each refined bin.
1. The size of refined bins and where its contigs come from.
1. You may want to run get_sankey_plot.R to visualize the correlations between your input bin sets (Figure below). To run it,
you need to have R and its following three packages installed: [tools](https://www.rdocumentation.org/packages/tools),
[optparse](https://cran.r-project.org/web/packages/optparse/index.html) and [googleVis](https://cran.r-project.org/web/packages/googleVis/index.html).

        # Example command
        Rscript get_sankey_plot.R -f GoogleVis_Sankey_0.5Mbp.csv -x 800 -y 1000

    ![Sankey_plot](images/sankey.jpg)

