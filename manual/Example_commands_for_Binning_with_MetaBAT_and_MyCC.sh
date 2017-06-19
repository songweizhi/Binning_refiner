
################################### 1 Quality Control #################################### 

# BBAY68, BBAY69 and BBAY70 are three replicate bacterial communities isolated from 
# the surface of the marine alga Caulerpa filiformis (Roth-Schulze et al., 2016). 
# The paired-end sequence data was generated on an Illumina HiSeq2000 platform.

# raw reads of three replicates
BBAY68_R1.fastq 
BBAY68_R2.fastq
BBAY69_R1.fastq 
BBAY69_R2.fastq
BBAY70_R1.fastq 
BBAY70_R2.fastq

# run trimmomatic to remove adapter sequences and bad quality reads
# http://www.usadellab.org/cms/uploads/supplementary/Trimmomatic/TrimmomaticManual_V0.32.pdf
java -jar /share/apps/trimmomatic/0.33/trimmomatic-0.33.jar PE BBAY68_R1.fastq BBAY68_R2.fastq BBAY68_R1_Q20_P.fastq BBAY68_R1_Q20_UP.fastq BBAY68_R2_Q20_P.fastq BBAY68_R2_Q20_UP.fastq ILLUMINACLIP:/share/apps/trimmomatic/0.33/adapters/TruSeq3-PE-2.fa:2:30:10:6:true LEADING:30 TRAILING:30 SLIDINGWINDOW:6:30 MINLEN:50
java -jar /share/apps/trimmomatic/0.33/trimmomatic-0.33.jar PE BBAY69_R1.fastq BBAY69_R2.fastq BBAY69_R1_Q20_P.fastq BBAY69_R1_Q20_UP.fastq BBAY69_R2_Q20_P.fastq BBAY69_R2_Q20_UP.fastq ILLUMINACLIP:/share/apps/trimmomatic/0.33/adapters/TruSeq3-PE-2.fa:2:30:10:6:true LEADING:30 TRAILING:30 SLIDINGWINDOW:6:30 MINLEN:50
java -jar /share/apps/trimmomatic/0.33/trimmomatic-0.33.jar PE BBAY70_R1.fastq BBAY70_R2.fastq BBAY70_R1_Q20_P.fastq BBAY70_R1_Q20_UP.fastq BBAY70_R2_Q20_P.fastq BBAY70_R2_Q20_UP.fastq ILLUMINACLIP:/share/apps/trimmomatic/0.33/adapters/TruSeq3-PE-2.fa:2:30:10:6:true LEADING:30 TRAILING:30 SLIDINGWINDOW:6:30 MINLEN:50

# run fastqc to check the quaities of filtered reads
# https://biof-edu.colorado.edu/videos/dowell-short-read-class/day-4/fastqc-manual
fastqc BBAY68_R1_Q30_P.fastq 
fastqc BBAY68_R2_Q30_P.fastq
fastqc BBAY69_R1_Q30_P.fastq 
fastqc BBAY69_R2_Q30_P.fastq
fastqc BBAY70_R1_Q30_P.fastq 
fastqc BBAY70_R2_Q30_P.fastq


################################ 2 Assemble with idba_ud ################################# 

# IDBA_UD
# http://i.cs.hku.hk/~alse/hkubrg/projects/idba_ud/

# combine the three first reads files (there will be 5 first reads files in your case)
cat BBAY68_R1_Q30_P.fastq BBAY69_R1_Q30_P.fastq BBAY70_R1_Q30_P.fastq > BBAY68_69_70_R1.fastq

# combine the three second reads files (there will be 5 second reads files in your case)
cat BBAY68_R2_Q30_P.fastq BBAY69_R2_Q30_P.fastq BBAY70_R2_Q30_P.fastq > BBAY68_69_70_R2.fastq

# convert and merge the two combined fastq files to fasta file with idba_ud. The output file will be used as input for assemble
fq2fa --merge BBAY68_69_70_R1.fastq BBAY68_69_70_R2.fastq BBAY68_69_70.fa

# run idba_ud, assembled contigs will be in the combined_k20-100/scaffold.fa file 
idba_ud --pre_correction --num_threads 3 --mink 20 --maxk 100 --step 20 --read BBAY68_69_70.fa --out combined_k20-100

# rename the assemblies
mv scaffold.fa BBAY68_69_70_K20-100_scaffold.fa

# remove short contigs (2500bp) from the scaffold.fa file with the select_contig.pl script
perl select_contig.pl -m 2500 BBAY68_69_70_K20-100_scaffold.fa BBAY68_69_70_K20-100_scaffold_lt2500.fa

# get contig statistics with get_fasta_stats.pl scripts
perl get_fasta_stats.pl -T BBAY68_69_70_K20-100_scaffold_lt2500.fa


####################################### 3 Mapping ######################################## 

# softwares needed:
# bowtie/2.2.9: http://bowtie-bio.sourceforge.net/bowtie2/manual.shtml
# samtools/1.2: http://samtools.sourceforge.net

# index assemblies with bowtie2
bowtie2-build -f BBAY68_69_70_K20-100_scaffold_lt2500.fa BBAY68_69_70_K20-100_scaffold_lt2500

# mapping with bowtie2
bowtie2 -x BBAY68_69_70_K20-100_scaffold_lt2500 -1 BBAY68_R1_Q30_P.fastq -2 BBAY68_R2_Q30_P.fastq -S BBAY68.sam -p 6 -q
bowtie2 -x BBAY68_69_70_K20-100_scaffold_lt2500 -1 BBAY69_R1_Q30_P.fastq -2 BBAY69_R2_Q30_P.fastq -S BBAY69.sam -p 6 -q
bowtie2 -x BBAY68_69_70_K20-100_scaffold_lt2500 -1 BBAY70_R1_Q30_P.fastq -2 BBAY70_R2_Q30_P.fastq -S BBAY70.sam -p 6 -q

# convert sam files to bam files with samtools
samtools view -bS BBAY68.sam -o BBAY68.bam
samtools view -bS BBAY69.sam -o BBAY69.bam
samtools view -bS BBAY70.sam -o BBAY70.bam

# sort bam files with samtools
samtools sort BBAY68.bam BBAY68_sorted
samtools sort BBAY69.bam BBAY69_sorted
samtools sort BBAY70.bam BBAY70_sorted

# index sorted bam files with samtools
samtools index BBAY68_sorted.bam
samtools index BBAY69_sorted.bam
samtools index BBAY70_sorted.bam


######################################## 4 Binning #######################################

# get depth file with Metabat (if your reads are paire-end, your might want to provide the "--pairedContigs" argument) 
jgi_summarize_bam_contig_depths --outputDepth BBAY68_69_70_depth.txt --pairedContigs BBAY68_69_70_paired.txt BBAY68_sorted.bam BBAY69_sorted.bam BBAY70_sorted.bam

# For MetaBAT
metabat -i BBAY68_69_70_K20-100_scaffold_lt2500.fa -a BBAY68_69_70_depth.txt -p depth/BBAY68_69_70_paired.txt -o BBAY68_69_70

# For MyCC (use ‘4mer’ for simple communities and ‘56mer’ for complex communities)
MyCC.py BBAY68_69_70_K20-100_scaffold_lt2500.fa -a BBAY68_69_70_depth.txt 56mer

# For CONCOCT
 

################################### 5 Binning_refiner #################################### 

# make a new folder named "Binning_refiner_wd", 
# copy all MetaBAT and MyCC produced bins into new folders named "MetaBAT" and "MyCC", respectively
# move the two bin folders into "Binning_refiner_wd", then run:
cd Binning_refiner_wd
Binning_refiner -1 MetaBAT -2 MyCC
CheckM_runner -1 MetaBAT -2 MyCC -r outputs/Refined -qsub

# after all submitted jobs in the CheckM_runner step were done, run
Get_statistics -1 MetaBAT -2 MyCC -r outputs/Refined -contamination_free_bin_completeness_cutoff 10

