Binning Refiner
---

+ This pipeline was developed to refine metagenomic bins by the combination of different binning programs.

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

1. Binning Refiner takes output bins from 2 different binning programs as inputs. It was developed to make your input
bins more "specific". You may need to try metagenomic binning steps with different parameters (like "verysensitive" and
"superspecific" for MetaBAT) to get the best output after refining (that is maximum contamination clearance and minimum
sequences lost). In my case, I can get more contamination-free bins (both of bin number and total length) with inputs
which are obtained from MetaBAT with "verysensitive" setting.

1. You need to define a working directory to hold all input and output files. Input bin sets from different
binning programs need to be placed in different folders directly under working directory.

1. Accepted bin file extensions include 'fa', 'fas' or 'fasta'. All input bins in the same folder must have the same extension.

1. Binning Refiner scripts are implemented in python3, please use python3 instead of python. These scripts have been
transferred to my home directory on Katana (/home/z5039045/Binning_refiner), you can call it directly from my home
directory. Any updates or bug-fix will be synchronized to this folder at first time.

1. (Reminder) As CheckM is a memory eating program, CheckM_qsuber.py will submit one job for each input/output bins.
This will become annoying if you have hundreds of bins, as the same number of emails will influx your email account!

        # Modules need to be loaded first:
        module load R/3.2.2
        module load python/3.4.3
        module load blast+/2.2.31

        # For help:
        python3 /home/z5039045/Binning_refiner/Binning_refiner.py -h
        python3 /home/z5039045/Binning_refiner/CheckM_qsuber.py -h
        python3 /home/z5039045/Binning_refiner/Get_statistics.py -h

        # Example commands:

        # 1. get refined bins
        python3 /home/z5039045/Binning_refiner/Binning_refiner.py -wd /.../test_data -f MetaBAT -s MyCC

        # 2. get qualities for each of the three bin sets
        python3 /home/z5039045/Binning_refiner/CheckM_qsuber.py -email your_email_address -i /.../test_data/MetaBAT
        python3 /home/z5039045/Binning_refiner/CheckM_qsuber.py -email your_email_address -i /.../test_data/MyCC
        python3 /home/z5039045/Binning_refiner/CheckM_qsuber.py -email your_email_address -i /.../test_data/outputs/Refined

        # 3. get statistics (after all submitted jobs in the 2nd step finished)
        python3 /home/z5039045/Binning_refiner/Get_statistics.py -f /.../test_data/MetaBAT -s /.../test_data/MyCC -r /.../test_data/outputs/Refined -o /.../test_data

Output files:
---

1. Refined bins (>= 0.5MB, from Binning_refiner.py)

1. Contamination-free refined bins (from Get_statistics.py)

1. Cross-link (shared sequences) between input bins (from Binning_refiner.py)

    ![Sankey_plot](doc/images/sankey_plot.jpg)

    Each band in the above image represents one refined bin, we will get 9 refined bins in this case:

        MetaBAT_bin2___MyCC_bin5.fasta   MetaBAT_bin1___MyCC_bin5.fasta   MetaBAT_bin6___MyCC_bin1.fasta
        MetaBAT_bin6___MyCC_bin4.fasta   MetaBAT_bin3___MyCC_bin1.fasta   MetaBAT_bin3___MyCC_bin4.fasta
        MetaBAT_bin4___MyCC_bin2.fasta   MetaBAT_bin5___MyCC_bin3.fasta   MetaBAT_bin5___MyCC_bin6.fasta

1. Statistics of input and refined bins (from Get_statistics.py)

    ![Statistics](doc/images/statistics.png)
