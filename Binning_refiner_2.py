import os
import glob
from time import sleep
import shutil
import argparse
from sys import stdout
from Bio import SeqIO
from lib.identity_list_ploter import plot_identity_list
from lib.GoogleVis_Sankey_plotter import GoogleVis_Sankey_plotter


##################################################### CONFIGURATION ####################################################

parser = argparse.ArgumentParser()

parser.add_argument('-1',
                    required=True,
                    help='first bin folder name')

parser.add_argument('-2',
                    required=True,
                    help='second bin folder name')

parser.add_argument('-3',
                    required=False,
                    help='third bin folder name')

parser.add_argument('-ms',
                    required=False,
                    default=524288,
                    type=int,
                    help='(optional) minimum size for refined bins, default = 524288 (0.5MB)')

args = vars(parser.parse_args())
input_bin_folder_1 = args['1']
if input_bin_folder_1[-1] == '/':
    input_bin_folder_1 = input_bin_folder_1[:-1]
input_bin_folder_2 = args['2']
if input_bin_folder_2[-1] == '/':
    input_bin_folder_2 = input_bin_folder_2[:-1]
if args['3'] != None:
    input_bin_folder_3 = args['3']
    if input_bin_folder_3[-1] == '/':
        input_bin_folder_3 = input_bin_folder_3[:-1]

bin_size_cutoff = args['ms']
bin_size_cutoff_MB = float("{0:.2f}".format(bin_size_cutoff / (1024 * 1024)))

# get input bin folder list
input_bin_folder_list = []
if args['3'] == None:
    print('Specified 2 input bin sets: -1 %s -2 %s' % (input_bin_folder_1, input_bin_folder_2))
    input_bin_folder_list = [input_bin_folder_1, input_bin_folder_2]
else:
    print('Specified 3 input bin sets: -1 %s -2 %s -3 %s' % (input_bin_folder_1, input_bin_folder_2, input_bin_folder_3))
    input_bin_folder_list = [input_bin_folder_1, input_bin_folder_2, input_bin_folder_3]


################################################ Define folder/file name ###############################################

wd = os.getcwd()
output_folder = 'outputs'
pwd_output_folder = '%s/%s' % (wd, output_folder)

########################################################################################################################


# get bin name list
bin_folder_1_bins_files = '%s/%s/*.fa*' % (wd, input_bin_folder_1)
bin_folder_2_bins_files = '%s/%s/*.fa*' % (wd, input_bin_folder_2)


# check input files
folder_bins_dict = {}
all_input_bins_list = []
all_input_bins_number_list = []
for bin_folder in input_bin_folder_list:
    bins_files = '%s/%s/*.fa*' % (wd, bin_folder)
    bin_folder_bins = [os.path.basename(file_name) for file_name in glob.glob(bins_files)]
    all_input_bins_list.append(bin_folder_bins)
    all_input_bins_number_list.append(len(bin_folder_bins))
    folder_bins_dict[bin_folder] = bin_folder_bins
    if len(bin_folder_bins) == 0:
        print('No input bin detected from %s folder, please double-check!' % (bin_folder))
        exit()

    bin_folder_bins_ext_list = []
    for bin in bin_folder_bins:
        bin_file_name, bin_file_ext = os.path.splitext(bin)
        bin_folder_bins_ext_list.append(bin_file_ext)

    bin_folder_bins_ext_list_uniq = []
    for each in bin_folder_bins_ext_list:
        if each not in bin_folder_bins_ext_list_uniq:
            bin_folder_bins_ext_list_uniq.append(each)
        else:
            pass
    # check whether bins in the same folder have same extension, exit if not
    if len(bin_folder_bins_ext_list_uniq) > 1:
        print('Different file extensions were found from %s bins, please use same extension (fa, fas or fasta) '
              'for all bins in the same folder.' % (bin_folder))
        exit()
    else:
        pass


# create output folder
if os.path.isdir(output_folder):
    shutil.rmtree(output_folder)
    os.mkdir(output_folder)
else:
    os.mkdir(output_folder)


# create folder to hold bins with renamed contig name
combined_all_bins_file = '%s/%s/combined_all_bins.fasta' % (wd, output_folder)
separator = '__'
for each_folder in input_bin_folder_list:
    os.mkdir('%s/%s/%s_new' % (wd, output_folder, each_folder))
    # add binning program and bin id to metabat_bin's contig name
    each_folder_bins = folder_bins_dict[each_folder]
    for each_bin in each_folder_bins:
        bin_file_name, bin_file_ext = os.path.splitext(each_bin)
        each_bin_content = SeqIO.parse('%s/%s/%s' % (wd, each_folder, each_bin), 'fasta')
        new = open('%s/%s/%s_new/%s_%s.fasta' % (wd, output_folder, each_folder, each_folder, bin_file_name), 'w')
        for each_contig in each_bin_content:
            each_contig_new_id = '%s%s%s%s%s' % (each_folder, separator, bin_file_name, separator, each_contig.id)
            each_contig.id = each_contig_new_id
            each_contig.description = ''
            SeqIO.write(each_contig, new, 'fasta')
        new.close()
    # Combine all new bins
    os.system('cat %s/%s/%s_new/*.fasta > %s/%s/combined_%s_bins.fa' % (wd, output_folder, each_folder, wd, output_folder, each_folder))
    os.system('rm -r %s/%s/%s_new' % (wd, output_folder, each_folder))
os.system('cat %s/%s/combined_*_bins.fa > %s' % (wd, output_folder, combined_all_bins_file))


combined_all_bins = SeqIO.parse(combined_all_bins_file, 'fasta')
contig_bin_dict = {}
contig_length_dict = {}
for each in combined_all_bins:
    each_id_split = each.id.split(separator)
    folder_name = each_id_split[0]
    bin_name = each_id_split[1]
    contig_id = each_id_split[2]
    length = len(each.seq)
    if contig_id not in contig_bin_dict:
        contig_bin_dict[contig_id] = ['%s%s%s' % (folder_name, separator, bin_name)]
        contig_length_dict[contig_id] = length
    elif contig_id in contig_bin_dict:
        contig_bin_dict[contig_id].append('%s%s%s' % (folder_name, separator, bin_name))
contig_assignments_file = '%s/%s/contig_assignments.txt' % (wd, output_folder)
contig_assignments = open(contig_assignments_file, 'w')


for each in contig_bin_dict:
    if len(contig_bin_dict[each]) == len(input_bin_folder_list):
        contig_assignments.write('%s\t%s\t%s\n' % ('\t'.join(contig_bin_dict[each]), each, contig_length_dict[each]))
contig_assignments.close()


contig_assignments_file_sorted = '%s/%s/contig_assignments_sorted.txt' % (wd, output_folder)
contig_assignments_file_sorted_one_line = '%s/%s/contig_assignments_sorted_one_line.txt' % (wd, output_folder)
os.system('cat %s | sort > %s' % (contig_assignments_file, contig_assignments_file_sorted))


contig_assignments_sorted = open(contig_assignments_file_sorted)
contig_assignments_sorted_one_line = open(contig_assignments_file_sorted_one_line, 'w')
current_match = ''
current_match_contigs = []
current_length_total = 0
n = 1
for each in contig_assignments_sorted:
    each_split = each.strip().split('\t')
    current_contig = each_split[-2]
    current_length = int(each_split[-1])
    matched_bins = '\t'.join(each_split[:-2])
    if current_match == '':
        current_match = matched_bins
        current_match_contigs.append(current_contig)
        current_length_total += current_length
    elif current_match == matched_bins:
        current_match_contigs.append(current_contig)
        current_length_total += current_length
    elif current_match != matched_bins:
        refined_bin_name = 'refined_bin%s' % n
        if current_length_total >= bin_size_cutoff:
            contig_assignments_sorted_one_line.write('Refined_%s\t%s\t%sbp\t%s\n' % (n, current_match, current_length_total,'\t'.join(current_match_contigs)))
            n += 1
        current_match = matched_bins
        current_match_contigs = []
        current_match_contigs.append(current_contig)
        current_length_total = 0
        current_length_total += current_length
if current_length_total >= bin_size_cutoff:
    contig_assignments_sorted_one_line.write('Refined_%s\t%s\t%sbp\t%s\n' % (n, current_match, current_length_total,'\t'.join(current_match_contigs)))
contig_assignments_sorted_one_line.close()
sleep(1)

# Export refined bins and prepare input for GoogleVis
print('Exporting refined bins and preparing input for GoogleVis sankey plot')
separated_1 = '%s/%s/Refined_bins_sources_and_length.txt' % (wd, output_folder)
separated_2 = '%s/%s/Refined_bins_contigs.txt' % (wd, output_folder)
googlevis_input_file = '%s/%s/GoogleVis_Sankey_%sMbp.csv' % (wd, output_folder, bin_size_cutoff_MB)
os.mkdir('%s/%s/Refined' % (wd, output_folder))
refined_bins = open(contig_assignments_file_sorted_one_line)
googlevis_input_handle = open(googlevis_input_file, 'w')
separated_1_handle = open(separated_1, 'w')
separated_2_handle = open(separated_2, 'w')

googlevis_input_handle.write('C1,C2,Length (Mbp)\n')
for each_refined_bin in refined_bins:
    each_refined_bin_split = each_refined_bin.strip().split('\t')
    each_refined_bin_name = each_refined_bin_split[0]
    each_refined_bin_length = 0
    each_refined_bin_contig = []
    if len(input_bin_folder_list) == 2:
        each_refined_bin_source = each_refined_bin_split[1:3]
        each_refined_bin_length = int(each_refined_bin_split[3][:-2])
        each_refined_bin_contig = each_refined_bin_split[4:]
        separated_1_handle.write('%s\t%sbp\t%s\n' % (each_refined_bin_name, each_refined_bin_length, '\t'.join(each_refined_bin_source)))
        separated_2_handle.write('%s\n%s\n' % (each_refined_bin_name, '\t'.join(each_refined_bin_contig)))


    if len(input_bin_folder_list) == 3:
        each_refined_bin_source = each_refined_bin_split[1:4]
        each_refined_bin_length = int(each_refined_bin_split[4][:-2])
        each_refined_bin_contig = each_refined_bin_split[5:]
        separated_1_handle.write('%s\t%sbp\t%s\n' % (each_refined_bin_name, each_refined_bin_length, '\t'.join(each_refined_bin_source)))
        separated_2_handle.write('%s\n%s\n' % (each_refined_bin_name, '\t'.join(each_refined_bin_contig)))
    each_refined_bin_length_mbp = float("{0:.2f}".format(each_refined_bin_length / (1024 * 1024)))
    m = 0
    while m < len(each_refined_bin_source)-1:
        googlevis_input_handle.write('%s,%s,%s\n' % (each_refined_bin_source[m], each_refined_bin_source[m+1], each_refined_bin_length_mbp))
        m += 1
    refined_bin_file = '%s/%s/Refined/%s.fasta' % (wd, output_folder, each_refined_bin_name)
    refined_bin_handle = open(refined_bin_file, 'w')
    input_contigs_file = '%s/%s/combined_%s_bins.fa' % (wd, output_folder, input_bin_folder_1)
    input_contigs = SeqIO.parse(input_contigs_file, 'fasta')
    for each_input_contig in input_contigs:
        each_input_contig_id = each_input_contig.id.split(separator)[-1]
        if each_input_contig_id in each_refined_bin_contig:
            SeqIO.write(each_input_contig, refined_bin_handle, 'fasta')
    refined_bin_handle.close()
googlevis_input_handle.close()
separated_1_handle.close()
separated_2_handle.close()

sleep(1)
# get GoogleVis Sankey plot
print('Plotting...')
sleep(1)
pwd_plot_html = '%s/%s/GoogleVis_Sankey_%sMbp.html' % (wd, output_folder, bin_size_cutoff_MB)
plot_height = max(all_input_bins_number_list) * 25
GoogleVis_Sankey_plotter(googlevis_input_file, pwd_plot_html, plot_height)
print('Please ignore "RRuntimeWarning" if there are any above.')
sleep(1)


# remove temporary files
print('Deleting temporary files')
os.system('rm %s' % contig_assignments_file)
os.system('rm %s' % (combined_all_bins_file))
os.system('rm %s/%s/*.fa' % (wd, output_folder))
os.system('rm %s' % (contig_assignments_file_sorted))
os.system('rm %s' % (googlevis_input_file))
os.system('rm %s' % (contig_assignments_file_sorted_one_line))

sleep(1)
print('All done!')
sleep(1)
print('Please run CheckM_qsuber.py for each input/output bin set to get their qualities.')