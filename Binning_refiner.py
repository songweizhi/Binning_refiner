import os
import glob
import shutil
import argparse
from sys import stdout
from Bio import SeqIO
#from lib.identity_list_ploter import plot_identity_list
from lib.GoogleVis_Sankey_plotter import GoogleVis_Sankey_plotter


steps = """"

    Steps:
    2. Combine MetaBAT and MyCC predicted bins respectively
    3. Make blast db
    4. Run Blast
    5. Filter blast hits
    6. Prepare input for googleVis
    7. Plot Sankey images
    8. get refined bins

"""

##################################################### CONFIGURATION ####################################################

parser = argparse.ArgumentParser()

parser.add_argument('-f',
                    required=True,
                    help='first bin folder name',
                    metavar='(req)')

parser.add_argument('-s',
                    required=True,
                    help='second bin folder name',
                    metavar='(req)')

parser.add_argument('-blastn',
                    required=False,
                    default='blastn',
                    help='path to blastn executable',
                    metavar='(opt)')

parser.add_argument('-makeblastdb',
                    required=False,
                    default='makeblastdb',
                    help='path to makeblastdb executable',
                    metavar='(opt)')

parser.add_argument('-bin_size_curoff',
                    required=False,
                    default=524288,
                    type=int,
                    help='length cutoff for refined bins, default = 524288 (0.5MB)',
                    metavar='(opt)')

args = parser.parse_args()
input_bin_folder_1 = args.f
if input_bin_folder_1[-1] == '/':
    input_bin_folder_1 = input_bin_folder_1[:-1]
input_bin_folder_2 = args.s
if input_bin_folder_2[-1] == '/':
    input_bin_folder_2 = input_bin_folder_2[:-1]
bin_size_cutoff = args.bin_size_curoff
bin_size_cutoff_MB = float("{0:.2f}".format(bin_size_cutoff / (1024 * 1024)))
pwd_blastn_exe = args.blastn
pwd_makeblastdb_exe = args.makeblastdb

########################################################################################################################


################################################ Define folder/file name ###############################################

wd = os.getcwd()

bin_folder_1_new =                  '%s_new'            % input_bin_folder_1
bin_folder_2_new =                  '%s_new'            % input_bin_folder_2
output_folder =                     'outputs'
blast_wd =                          'Blast_wd'

# blast_results_folder =              'Blast_results'
googlevis_input_filename =          'googleVis_%s_vs_%s_all.csv'              % (input_bin_folder_1, input_bin_folder_2)
googlevis_input_filtered_filename = 'googleVis_%s_vs_%s_size_cutoff_%sMB.csv'  % (input_bin_folder_1, input_bin_folder_2, bin_size_cutoff_MB)
plot_html =                         'googleVis_%s_vs_%s_all.html'              % (input_bin_folder_1, input_bin_folder_2)
plot_html_filtered =                'googleVis_%s_vs_%s_size_cutoff_%sMB.html'  % (input_bin_folder_1, input_bin_folder_2, bin_size_cutoff_MB)
new_bin_contigs_filename =          'Contigs_in_refined_bins.txt'
refined_bins_folder =               'Refined'

pwd_output_folder =             '%s/%s'     % (wd, output_folder)
pwd_bin_folder_1_new =          '%s/%s/%s'  % (wd, blast_wd, bin_folder_1_new)
pwd_bin_folder_2_new =          '%s/%s/%s'  % (wd, blast_wd, bin_folder_2_new)
pwd_blast_wd =                  '%s/%s'     % (wd, blast_wd)
# pwd_blast_results_folder =      '%s/%s/%s'  % (wd, output_folder, blast_results_folder)
pwd_googlevis_input =           '%s/%s/%s'  % (wd, output_folder, googlevis_input_filename)
pwd_googlevis_input_filtered =  '%s/%s/%s'  % (wd, output_folder, googlevis_input_filtered_filename)
pwd_plot_html =                 '%s/%s/%s'  % (wd, output_folder, plot_html)
pwd_plot_html_filtered =        '%s/%s/%s'  % (wd, output_folder, plot_html_filtered)
pwd_new_bin_contigs =           '%s/%s/%s'  % (wd, output_folder, new_bin_contigs_filename)
pwd_refined_bins_folder =       '%s/%s/%s'  % (wd, output_folder, refined_bins_folder)


blast_result = 'blast_%s_vs_%s.tab' % (input_bin_folder_1, input_bin_folder_2)
pwd_blast_result = '%s/%s' % (pwd_blast_wd, blast_result)
combined_folder1_bins = 'combined_%s_bins.fasta' % input_bin_folder_1
pwd_combined_folder1_bins = '%s/%s' % (pwd_blast_wd, combined_folder1_bins)
combined_folder2_bins = 'combined_%s_bins.fasta' % input_bin_folder_2
pwd_combined_folder2_bins = '%s/%s' % (pwd_blast_wd, combined_folder2_bins)

########################################################################################################################


def run_blast():
    # create folder to hold bins with renamed contig name
    os.mkdir(pwd_blast_wd)
    os.mkdir(pwd_bin_folder_1_new)
    os.mkdir(pwd_bin_folder_2_new)

    # add binning program and bin id to metabat_bin's contig name
    print('Adding binning program and bin id to contig name')
    for metabat_bin in bin_folder_1_bins:
        bin_name_metabat, ext = os.path.splitext(metabat_bin)
        bin_content = SeqIO.parse('%s/%s/%s' % (wd, input_bin_folder_1, metabat_bin), 'fasta')
        new = open('%s/%s/%s/%s_%s.fasta' % (wd, blast_wd, bin_folder_1_new, input_bin_folder_1, bin_name_metabat), 'w')
        for contig in bin_content:
            new_id = '%s__%s__%s' % (input_bin_folder_1, bin_name_metabat, contig.id)
            contig.id = new_id
            contig.description = ''
            SeqIO.write(contig, new, 'fasta')
        new.close()

    # add binning program and bin id to mycc_bin's contig name
    for mycc_bin in bin_folder_2_bins:
        bin_name_mycc, ext = os.path.splitext(mycc_bin)
        bin_content = SeqIO.parse('%s/%s/%s' % (wd, input_bin_folder_2, mycc_bin), 'fasta')

        new = open('%s/%s/%s/%s_%s.fasta' % (wd, blast_wd, bin_folder_2_new, input_bin_folder_2, bin_name_mycc), 'w')
        for contig in bin_content:
            new_id = '%s__%s__%s' % (input_bin_folder_2, bin_name_mycc, contig.id)
            contig.id = new_id
            contig.description = ''
            SeqIO.write(contig, new, 'fasta')
        new.close()

    # Combine all MetaBAT and MyCC bins, respectively
    os.system('cat %s/*.fasta > %s' % (pwd_bin_folder_1_new, pwd_combined_folder1_bins))
    os.system('cat %s/*.fasta > %s' % (pwd_bin_folder_2_new, pwd_combined_folder2_bins))
    os.system('rm -r ./%s/%s' % (blast_wd, bin_folder_1_new))
    os.system('rm -r ./%s/%s' % (blast_wd, bin_folder_2_new))

    # make blast database
    print('Making Blastdb with %s' % combined_folder2_bins)
    os.system('%s -in %s -dbtype nucl -parse_seqids' % (pwd_makeblastdb_exe, pwd_combined_folder2_bins))
    outfmt = '-outfmt "6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore qlen slen"'
    print('\nRunning Blast, be patient...')
    os.system('%s -query %s -db %s -out %s -perc_identity 100 %s' % (
    pwd_blastn_exe, pwd_combined_folder1_bins, pwd_combined_folder2_bins, pwd_blast_result, outfmt))


# get bin name list
bin_folder_1_bins_files = '%s/%s/*.fa*' % (wd, input_bin_folder_1)
bin_folder_2_bins_files = '%s/%s/*.fa*' % (wd, input_bin_folder_2)

bin_folder_1_bins = [os.path.basename(file_name) for file_name in glob.glob(bin_folder_1_bins_files)]
if len(bin_folder_1_bins) == 0:
    print('No input bin detected from %s/%s, please double-check' % (wd, input_bin_folder_1))
    exit()

bin_folder_1_bins_ext_list = []
for bin_folder_1_bin in bin_folder_1_bins:
    name_no_use, ext = os.path.splitext(bin_folder_1_bin)
    bin_folder_1_bins_ext_list.append(ext)

bin_folder_1_bins_ext_list_uniq = []
for each in bin_folder_1_bins_ext_list:
    if each not in bin_folder_1_bins_ext_list_uniq:
        bin_folder_1_bins_ext_list_uniq.append(each)
    else:
        pass

# check whether bins in the same folder have same extension, exit if not
if len(bin_folder_1_bins_ext_list_uniq) > 1:
    print('Different bin file extensions were detected from bins in %s/%s, please use same extension (fa, fas or fasta) '
          'for each bin in same bin sets.' % (wd, input_bin_folder_1))
    exit()
else:
    pass


bin_folder_2_bins = [os.path.basename(file_name) for file_name in glob.glob(bin_folder_2_bins_files)]
if len(bin_folder_2_bins) == 0:
    print('No input bin detected from %s/%s, please double-check' % (wd, input_bin_folder_2))
    exit()

bin_folder_2_bins_ext_list = []
for bin_folder_2_bin in bin_folder_2_bins:
    name_no_use, ext = os.path.splitext(bin_folder_2_bin)
    bin_folder_2_bins_ext_list.append(ext[1:])

bin_folder_2_bins_ext_list_uniq = []
for each in bin_folder_2_bins_ext_list:
    if each not in bin_folder_2_bins_ext_list_uniq:
        bin_folder_2_bins_ext_list_uniq.append(each)
    else:
        pass

if len(bin_folder_2_bins_ext_list_uniq) > 1:
    print('Different bin file extensions were detected from bins in %s/%s, please use same extension (fa, fas or fasta) '
          'for each bin in same bin sets.' % (wd, input_bin_folder_2))
    exit()
else:
    pass

# remove existing output folder, if any
if os.path.isdir(output_folder):
    shutil.rmtree(output_folder)


if os.path.isfile(pwd_blast_result):
    choice = str(input('Blast results detected, Press "S/s" to skip blast step, Press any other key to overwrite it.\nYour choice: '))
    if choice in ['s', 'S']:
        pass
    else:
        shutil.rmtree(pwd_blast_wd)
        run_blast()
else:
    run_blast()

# create output folder
if not os.path.isdir(output_folder):
    os.mkdir(output_folder)
    # os.mkdir(pwd_blast_results_folder)
else:
    shutil.rmtree(output_folder)
    os.mkdir(output_folder)
    # os.mkdir(pwd_blast_results_folder)


# filter blast results
print('Blast finished, processing blast results')
blast_result = open(pwd_blast_result)
blast_result_filtered_1_filename = 'blast_%s_vs_%s_filtered_1.tab' % (input_bin_folder_1, input_bin_folder_2)
blast_result_filtered_2_filename = 'blast_%s_vs_%s_filtered_2.tab' % (input_bin_folder_1, input_bin_folder_2)
pwd_blast_result_filtered_1 = '%s/%s/%s' % (wd, output_folder, blast_result_filtered_1_filename)
pwd_blast_result_filtered_2 = '%s/%s/%s' % (wd, output_folder, blast_result_filtered_2_filename)
blast_result_filtered_1 = open(pwd_blast_result_filtered_1, 'w')
blast_result_filtered_2 = open(pwd_blast_result_filtered_2, 'w')
for match in blast_result:
    match_split = match.strip().split('\t')
    query = match_split[0]
    query_split = query.split('__')
    query_bin = query_split[1]
    query_scaffold = query_split[2]
    subject = match_split[1]
    subject_split = subject.split('__')
    subject_bin = subject_split[1]
    subject_scaffold = subject_split[2]
    identity = float(match_split[2])
    alignment_len = int(match_split[3])
    query_len = int(match_split[12])
    subject_len = int(match_split[13])
    if (identity == 100) and (query_len == subject_len == alignment_len) and (query_scaffold == subject_scaffold):
        blast_result_filtered_1.write(match)
        needed_with_contig = '%s\t%s\t%s\t%s\n' % (query_bin, subject_bin, query_scaffold, alignment_len)
        blast_result_filtered_2.write(needed_with_contig)
blast_result_filtered_1.close()
blast_result_filtered_2.close()

# sort filtered blast results
blast_result_filtered_2_sorted_filename = 'blast_%s_against_%s_filtered_2_sorted.tab' % (input_bin_folder_1, input_bin_folder_2)
pwd_blast_result_filtered_2_sorted = '%s/%s/%s' % (wd, output_folder, blast_result_filtered_2_sorted_filename)
os.system('cat %s | sort > %s' % (pwd_blast_result_filtered_2, pwd_blast_result_filtered_2_sorted))
os.system('rm ./%s/%s' % (output_folder, blast_result_filtered_1_filename))
os.system('rm ./%s/%s' % (output_folder, blast_result_filtered_2_filename))

# get total length between bins
print('Preparing input for GoogleVis sankey plot\n')
sorted = open(pwd_blast_result_filtered_2_sorted)
googlevis_input = open(pwd_googlevis_input, 'w')
googlevis_input_filtered = open(pwd_googlevis_input_filtered, 'w')
new_bin_contigs = open(pwd_new_bin_contigs, 'w')
new_bin_contigs.write('Refined_bin_name\tRefined_bin_length\tContigs_in_refined_bin\n')

googlevis_input.write('%s,%s,Length_in_MB\n' % (input_bin_folder_1, input_bin_folder_2))
googlevis_input_filtered.write('%s,%s,Length_in_MB\n' % (input_bin_folder_1, input_bin_folder_2))

current_match = ''
current_match_under_score = ''
current_length = 0
current_contig_list = []
# bin_size_list = []
# bin_size_list_filtered = []
for each in sorted:
    each_split = each.strip().split('\t')
    query_bin = each_split[0]
    subject_bin = each_split[1]
    contig_id = each_split[2]
    alignment_len_2 = int(each_split[3])
    match_pair = query_bin + ',' + subject_bin
    match_pair_under_score = query_bin + '___' + subject_bin
    if current_match == '':
        current_match = match_pair
        current_match_under_score = match_pair_under_score
        current_length += alignment_len_2
        current_contig_list.append(contig_id)
    elif current_match == match_pair:
        current_length += alignment_len_2
        current_contig_list.append(contig_id)
    elif current_match != match_pair:
        current_length_MB = float("{0:.2f}".format(current_length / (1024 * 1024)))
        googlevis_input.write('%s,%s\n' % (current_match, current_length_MB))
        new_bin_contigs.write('%s\t%s\t%s\n' % (current_match_under_score, current_length, '\t'.join(current_contig_list)))
        # bin_size_list.append(current_length)
        if current_length >= bin_size_cutoff:
            # bin_size_list_filtered.append(current_length)
            #current_length = current_length/(1024*1024)
            googlevis_input_filtered.write('%s,%s\n' % (current_match, current_length_MB))
        current_length = alignment_len_2
        current_match = match_pair
        current_match_under_score = match_pair_under_score
        current_contig_list = []
        current_contig_list.append(contig_id)

current_length_MB = float("{0:.2f}".format(current_length / (1024 * 1024)))
googlevis_input.write('%s,%s\n' % (current_match, current_length_MB))
new_bin_contigs.write('%s\t%s\t%s\n' % (current_match_under_score, current_length, '\t'.join(current_contig_list)))
# bin_size_list.append(current_length)
if current_length >= bin_size_cutoff:
    # bin_size_list_filtered.append(current_length)
    googlevis_input_filtered.write('%s,%s\n' % (current_match, current_length_MB))
googlevis_input.close()
new_bin_contigs.close()
googlevis_input_filtered.close()

# plot size distribution of all new bins
# plot_identity_list(bin_size_list, bin_size_cutoff, 'Bin Size Distribution', pwd_output_folder)
# plot_identity_list(bin_size_list_filtered, bin_size_cutoff, 'Bin Size Distribution (cutoff' + str(bin_size_cutoff) + 'bp)', pwd_output_folder)

# plot googlevis image
print('Plotting...')
plot_height = max([len(bin_folder_1_bins), len(bin_folder_2_bins)]) * 40
GoogleVis_Sankey_plotter(pwd_googlevis_input, pwd_plot_html, plot_height)
GoogleVis_Sankey_plotter(pwd_googlevis_input_filtered, pwd_plot_html_filtered, plot_height)
print('Please ignore "RRuntimeWarning" if there are any above.')

# get new bins and filter with size
print('Extracting contigs for new bins:')
os.mkdir(pwd_refined_bins_folder)

# get total number of refined bins
new_bins = open(pwd_googlevis_input_filtered)
total = -1  # remove title line
for each_new_bin in new_bins:
    total += 1

new_bins = open(pwd_new_bin_contigs) ###!!!!!!!!!!!!
n = 1
for each_new_bin in new_bins:
    if not each_new_bin.startswith('Refined_bin_name'):
        each_new_bin_split = each_new_bin.strip().split('\t')
        new_bin_name = each_new_bin_split[0]
        new_bin_size = int(each_new_bin_split[1])
        new_bin_contig_list = each_new_bin_split[2:]
        if new_bin_size >= bin_size_cutoff:
            stdout.write("\rProcessing %dth of %d refined new bins: %s" % (n, total, new_bin_name))
            fasta_handle = open('%s/%s.fasta' % (pwd_refined_bins_folder, new_bin_name), 'w')
            all_contigs = SeqIO.parse(pwd_combined_folder1_bins, 'fasta')
            for each_contig in all_contigs:
                new_contig_id = each_contig.id.split('__')[2]
                each_contig.id = new_contig_id
                each_contig.description = ''
                if each_contig.id in new_bin_contig_list:
                    SeqIO.write(each_contig, fasta_handle, 'fasta')
            fasta_handle.close()
            n += 1

# remove temporary files
os.system('mv ./%s/%s ./%s/Shared_contigs_between_%s_and_%s_bins.txt' % (output_folder, blast_result_filtered_2_sorted_filename, output_folder, input_bin_folder_1, input_bin_folder_2))


print('\nDone!')
print('Please run CheckM_qsuber.py for each input/output bin set to get their quality.')
