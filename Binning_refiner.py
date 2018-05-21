# Copyright (C) 2017, Weizhi Song, Torsten Thomas.
# songwz03@gmail.com or t.thomas@unsw.edu.au

# Binning_refiner is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Binning_refiner is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import glob
import shutil
import argparse
from Bio import SeqIO
from time import sleep
from datetime import datetime

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

parser.add_argument('-x1',
                    required=False,
                    default='fasta',
                    help='file extension for bin set 1, default: fasta')

parser.add_argument('-x2',
                    required=False,
                    default='fasta',
                    help='file extension for bin set 2, default: fasta')

parser.add_argument('-x3',
                    required=False,
                    default='fasta',
                    help='file extension for bin set 3, default: fasta')

parser.add_argument('-prefix',
                    required=False,
                    default='Refined',
                    help='prefix of refined bins, default: Refined')

parser.add_argument('-ms',
                    required=False,
                    default=524288,
                    type=int,
                    help='minimal size for refined bins, default = 524288 (0.5Mbp)')

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

bin_extension_1 = args['x1']
bin_extension_2 = args['x2']
bin_extension_3 = args['x3']
prefix = args['prefix']
bin_size_cutoff = args['ms']
bin_size_cutoff_MB = float("{0:.2f}".format(bin_size_cutoff / (1024 * 1024)))

# get input bin folder list
input_bin_folder_list = []
if args['3'] == None:
    sleep(1)
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Specified 2 input bin sets:\n-1 %s\n-2 %s' % (input_bin_folder_1, input_bin_folder_2))
    input_bin_folder_list = [input_bin_folder_1, input_bin_folder_2]
    input_bin_extension_list = [bin_extension_1, bin_extension_2]

else:
    sleep(1)
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Specified 3 input bin sets:\n                    -1 %s\n                    -2 %s\n                    -3 %s' % (input_bin_folder_1, input_bin_folder_2, input_bin_folder_3))
    input_bin_folder_list = [input_bin_folder_1, input_bin_folder_2, input_bin_folder_3]
    input_bin_extension_list = [bin_extension_1, bin_extension_2, bin_extension_3]

input_bin_folder_name_list = []
for each_bin_folder in input_bin_folder_list:
    bin_folder_name = each_bin_folder.split('/')[-1]
    input_bin_folder_name_list.append(bin_folder_name)

sleep(1)
print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' The minimal size for refined bins was set to %s bp.' % (bin_size_cutoff))

################################################ Define folder/file name ###############################################

pwd_output_folder = '%s_outputs' % prefix
refined_bin_folder = 'Refined_bins'
pwd_refined_bin_folder = '%s/%s' % (pwd_output_folder, refined_bin_folder)

########################################################################################################################

# check input files
folder_bins_dict = {}
all_input_bins_list = []
all_input_bins_number_list = []
n = 0
for bin_folder in input_bin_folder_list:
    bin_folder_name = bin_folder.split('/')[-1]
    bins_files = '%s/*.%s' % (bin_folder, input_bin_extension_list[n])
    bin_folder_bins = [os.path.basename(file_name) for file_name in glob.glob(bins_files)]
    all_input_bins_list.append(bin_folder_bins)
    all_input_bins_number_list.append(len(bin_folder_bins))
    folder_bins_dict[bin_folder_name] = bin_folder_bins
    if len(bin_folder_bins) == 0:
        sleep(1)
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' No input bin detected from %s folder, please double-check! Pay attention to file extension, default: fasta' % (bin_folder))
        exit()

    bin_folder_bins_ext_list = []
    for bin in bin_folder_bins:
        bin_file_name, bin_file_ext = os.path.splitext(bin)
        bin_folder_bins_ext_list.append(bin_file_ext)

    bin_folder_bins_ext_list_uniq = []
    for each in bin_folder_bins_ext_list:
        if each not in bin_folder_bins_ext_list_uniq:
            bin_folder_bins_ext_list_uniq.append(each)

    # check whether bins in the same folder have same extension, exit if not
    if len(bin_folder_bins_ext_list_uniq) > 1:
        sleep(1)
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Different file extensions were found from %s bins, please use same extension (fa, fas or fasta) '
              'for all bins in the same folder.' % (bin_folder))
        exit()
    n += 1


# create output folder
if os.path.isdir(pwd_output_folder):
    shutil.rmtree(pwd_output_folder)
    os.mkdir(pwd_output_folder)
    os.mkdir(pwd_refined_bin_folder)
else:
    os.mkdir(pwd_output_folder)
    os.mkdir(pwd_refined_bin_folder)


# create folder to hold bins with renamed contig name
sleep(1)
print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Rename input bins')
combined_all_bins_file = '%s/combined_all_bins.fasta' % (pwd_output_folder)
separator = '__'
for each_folder in input_bin_folder_list:
    sleep(1)
    each_folder_name = each_folder.split('/')[-1]

    os.mkdir('%s/%s_new' % (pwd_output_folder, each_folder_name))
    # add binning program and bin id to metabat_bin's contig name
    each_folder_bins = folder_bins_dict[each_folder_name]
    for each_bin in each_folder_bins:
        bin_file_name, bin_file_ext = os.path.splitext(each_bin)
        each_bin_content = SeqIO.parse('%s/%s' % (each_folder, each_bin), 'fasta')
        new = open('%s/%s_new/%s_%s.fasta' % (pwd_output_folder, each_folder_name, each_folder_name, bin_file_name), 'w')
        for each_contig in each_bin_content:
            each_contig_new_id = '%s%s%s%s%s' % (each_folder_name, separator, bin_file_name, separator, each_contig.id)
            each_contig.id = each_contig_new_id
            each_contig.description = ''
            SeqIO.write(each_contig, new, 'fasta')
        new.close()
    # Combine all new bins
    os.system('cat %s/%s_new/*.fasta > %s/combined_%s_bins.fa' % (pwd_output_folder, each_folder_name, pwd_output_folder, each_folder_name))
    os.system('rm -r %s/%s_new' % (pwd_output_folder, each_folder_name))

# combine all modified bins together
sleep(1)
print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Combine all bins together')
if len(input_bin_folder_list) == 2:
    pwd_combined_folder_1_bins = '%s/combined_%s_bins.fa' % (pwd_output_folder, input_bin_folder_1.split('/')[-1])
    pwd_combined_folder_2_bins = '%s/combined_%s_bins.fa' % (pwd_output_folder, input_bin_folder_2.split('/')[-1])
    os.system('cat %s %s > %s' % (pwd_combined_folder_1_bins, pwd_combined_folder_2_bins, combined_all_bins_file))

if len(input_bin_folder_list) == 3:
    pwd_combined_folder_1_bins = '%s/combined_%s_bins.fa' % (pwd_output_folder, input_bin_folder_1.split('/')[-1])
    pwd_combined_folder_2_bins = '%s/combined_%s_bins.fa' % (pwd_output_folder, input_bin_folder_2.split('/')[-1])
    pwd_combined_folder_3_bins = '%s/combined_%s_bins.fa' % (pwd_output_folder, input_bin_folder_3.split('/')[-1])
    os.system('cat %s %s %s > %s' % (pwd_combined_folder_1_bins, pwd_combined_folder_2_bins, pwd_combined_folder_3_bins, combined_all_bins_file))

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
contig_assignments_file = '%s/contig_assignments.txt' % (pwd_output_folder)
contig_assignments = open(contig_assignments_file, 'w')


for each in contig_bin_dict:
    if len(contig_bin_dict[each]) == len(input_bin_folder_list):
        contig_assignments.write('%s\t%s\t%s\n' % ('\t'.join(contig_bin_dict[each]), each, contig_length_dict[each]))

contig_assignments.close()


contig_assignments_file_sorted = '%s/contig_assignments_sorted.txt' % (pwd_output_folder)
contig_assignments_file_sorted_one_line = '%s/contig_assignments_sorted_one_line.txt' % (pwd_output_folder)
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
        if current_length_total >= bin_size_cutoff:
            contig_assignments_sorted_one_line.write('%s_%s\t%s\t%sbp\t%s\n' % (prefix, n, current_match, current_length_total,'\t'.join(current_match_contigs)))
            n += 1
        current_match = matched_bins
        current_match_contigs = []
        current_match_contigs.append(current_contig)
        current_length_total = 0
        current_length_total += current_length
if current_length_total >= bin_size_cutoff:
    contig_assignments_sorted_one_line.write('%s_%s\t%s\t%sbp\t%s\n' % (prefix, n, current_match, current_length_total,'\t'.join(current_match_contigs)))
else:
    n -= 1
contig_assignments_sorted_one_line.close()

refined_bin_number = n
sleep(1)
print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' The number of refined bins: %s' % refined_bin_number)

# Export refined bins and prepare input for GoogleVis
sleep(1)
separated_1 = '%s/Refined_bins_sources_and_length.txt' % (pwd_output_folder)
separated_2 = '%s/Refined_bins_contigs.txt' % (pwd_output_folder)
googlevis_input_file = '%s/GoogleVis_Sankey_%sMbp.csv' % (pwd_output_folder, bin_size_cutoff_MB)
refined_bins = open(contig_assignments_file_sorted_one_line)
googlevis_input_handle = open(googlevis_input_file, 'w')
separated_1_handle = open(separated_1, 'w')
separated_2_handle = open(separated_2, 'w')

googlevis_input_handle.write('C1,C2,Length_Mbp\n')
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

    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Extracting %s.fasta' % each_refined_bin_name)
    refined_bin_file = '%s/%s.fasta' % (pwd_refined_bin_folder, each_refined_bin_name)
    refined_bin_handle = open(refined_bin_file, 'w')
    input_contigs_file = '%s/combined_%s_bins.fa' % (pwd_output_folder, input_bin_folder_1.split('/')[-1])
    for each_input_contig in SeqIO.parse(input_contigs_file, 'fasta'):
        each_input_contig_id = each_input_contig.id.split(separator)[-1]
        if each_input_contig_id in each_refined_bin_contig:
            each_input_contig.id = each_input_contig_id
            each_input_contig.description = ''
            SeqIO.write(each_input_contig, refined_bin_handle, 'fasta')
    refined_bin_handle.close()
googlevis_input_handle.close()
separated_1_handle.close()
separated_2_handle.close()

# remove temporary files
sleep(1)
print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Deleting temporary files')
os.system('rm %s' % contig_assignments_file)
os.system('rm %s' % (combined_all_bins_file))
os.system('rm %s/*.fa' % (pwd_output_folder))
os.system('rm %s' % (contig_assignments_file_sorted))
os.system('rm %s' % (contig_assignments_file_sorted_one_line))

sleep(1)
print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' All done!')
sleep(1)
print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Things you may want to do:')
print('                    1. Run get_sankey_plot.R to visualize the correlations between your input bin sets with:')
plot_width = 500
if len(input_bin_folder_list) == 3:
    plot_width = 700
plot_height = max(all_input_bins_number_list) * 30
print('                       Rscript get_sankey_plot.R -f GoogleVis_Sankey_%sMbp.csv -x %s -y %s' % (bin_size_cutoff_MB, plot_width, plot_height))
print('                    2. Run CheckM to get the quality of your input and refined bins.')
