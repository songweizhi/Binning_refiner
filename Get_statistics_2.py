import os
import glob
import shutil
import argparse
import numpy as np
from scipy import stats
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from lib.get_array import get_array
from lib.get_bin_size import get_bin_size
from lib.get_bin_statistics import get_bin_statistics

#################################################### CONFIGURATION #####################################################

parser = argparse.ArgumentParser()

parser.add_argument('-1',
                    help='first bin folder name',
                    required=True)

parser.add_argument('-2',
                    help='second bin folder name',
                    required=True)

parser.add_argument('-3',
                    help='third bin folder name',
                    required=False)

parser.add_argument('-r',
                    help='refined bin folder name',
                    required=True)

parser.add_argument('-ms',
                    required=False,
                    default=524288,
                    type=int,
                    help='(optional) minimum size for refined bins, default = 524288 (0.5MB)')

parser.add_argument('-good_bin_completeness',
                    required=False,
                    default=70,
                    type=int,
                    help='(optional) the completeness cutoff of good bins')

parser.add_argument('-good_bin_contamination',
                    required=False,
                    default=5,
                    type=int,
                    help='(optional) the contamination cutoff of good bins')


args = vars(parser.parse_args())

input_bin_folder_list = []

input_bin_folder_1 = args['1']
if input_bin_folder_1[-1] == '/':
    input_bin_folder_1 = input_bin_folder_1[:-1]
input_bin_folder_list.append(input_bin_folder_1)


input_bin_folder_2 = args['2']
if input_bin_folder_2[-1] == '/':
    input_bin_folder_2 = input_bin_folder_2[:-1]
input_bin_folder_list.append(input_bin_folder_2)


if args['3'] != None:
    input_bin_folder_3 = args['3']
    if input_bin_folder_3[-1] == '/':
        input_bin_folder_3 = input_bin_folder_3[:-1]
    input_bin_folder_list.append(input_bin_folder_3)


input_refined_bin_folder = args['r']
if input_refined_bin_folder[-1] == '/':
    input_refined_bin_folder = input_refined_bin_folder[:-1]
input_bin_folder_list.append(input_refined_bin_folder)

bin_size_cutoff = int(args['ms'])


########################################################################################################################

# define folder/file name
wd = os.getcwd()
checkm_wd_name = 'checkm_wd'
contamination_free_refined_bin_folder = 'contamination_free_refined_bins'
statistics_txt_filename = 'Bin_qualities_overall.txt'
pwd_statistics_txt = '%s/%s' % (wd, statistics_txt_filename)
pwd_contamination_free_refined_bin_folder = '%s/%s' % (args['r'], contamination_free_refined_bin_folder)
pwd_statistics_image = '%s/outputs/Bin_qualities.png' % (wd)

#################################################### Get input data ####################################################


for each_bin_folder in input_bin_folder_list:
    pwd_each_bin_folder = '%s/%s' % (wd, each_bin_folder)
    each_bin_folder_bin_files = '%s/*.fa*' % pwd_each_bin_folder
    each_bin_folder_bin_list = [os.path.basename(file_name) for file_name in glob.glob(each_bin_folder_bin_files)]

    if len(each_bin_folder_bin_list) == 0:
        print('No input bin detected from %s, please double-check.' % each_bin_folder)
        exit()

    bin_file_ext_list = []
    for bin in each_bin_folder_bin_list:
        name, ext = os.path.splitext(bin)
        bin_file_ext_list.append(ext[1:])

    # uniq bin_file_ext_list
    bin_file_ext_list_uniq = []
    for each in bin_file_ext_list:
        if each not in bin_file_ext_list_uniq:
            bin_file_ext_list_uniq.append(each)
        else:
            pass

    # check whether bins in the same folder have same extension, exit if not
    if len(bin_file_ext_list_uniq) > 1:
        print('Different bin file extensions were detected from bins in %s, please use same extension (fa, fas or fasta) '
              'for each bin sets.' % each_bin_folder)
        exit()
    else:
        pass

    # # get bin file extension
    # bin_file_extension = bin_file_ext_list_uniq[0]
    pwd_quality_file = ''
    if '/' in each_bin_folder:
        each_bin_folder_split = each_bin_folder.split('/')
        pwd_quality_file_unploted = '%s/%s/Bin_qualities_%s_unploted.txt' % (wd, 'outputs', each_bin_folder_split[-1])
        pwd_quality_file_qualified = '%s/%s/Bin_qualities_%s_qualified.txt' % (wd, 'outputs', each_bin_folder_split[-1])
    else:
        pwd_quality_file_unploted = '%s/%s/Bin_qualities_%s_unploted.txt' % (wd, 'outputs', each_bin_folder)
        pwd_quality_file_qualified = '%s/%s/Bin_qualities_%s_qualified.txt' % (wd, 'outputs', each_bin_folder)

    quality_file_handle_unploted = open(pwd_quality_file_unploted, 'w')
    quality_file_handle_qualified = open(pwd_quality_file_qualified, 'w')

    quality_file_handle_unploted.write('Bin_name\tMarker_lineage\tBin_size(Mbp)\tCompleteness\tContamination\tHeterogeneity\n')
    quality_file_handle_qualified.write('Bin_name\tMarker_lineage\tBin_size(Mbp)\tCompleteness\tContamination\tHeterogeneity\n')

    unploted_bin_number = 0
    for each_bin in each_bin_folder_bin_list:
        each_bin_name, ext = os.path.splitext(each_bin)
        pwd_bin_file = '%s/%s/%s' % (wd, each_bin_folder,each_bin)
        pwd_bin_quality_file = '%s/%s/%s/%s.txt' % (wd, each_bin_folder, checkm_wd_name, each_bin_name)

        bin_size = get_bin_size(pwd_bin_file)
        bin_size_Mbp = float("{0:.2f}".format(bin_size / (1024 * 1024)))
        #print(bin_size_Mbp)

        # check whether quality file exist
        if os.path.isfile(pwd_bin_quality_file):
            bin_quality = open(pwd_bin_quality_file)
            for quality in bin_quality:
                if (quality.startswith('--')) or (quality.startswith('  Bin Id')):
                    pass
                else:
                    quality_split = quality.strip().split(' ')
                    quality_split_new = []
                    for each in quality_split:
                        if each != '':
                            quality_split_new.append(each)
                    #print(quality_split_new)
                    bin_name = quality_split_new[0]
                    Marker_lineage = quality_split_new[1]
                    completeness = float(quality_split_new[12])
                    contamination = float(quality_split_new[13])
                    Heterogeneity = float(quality_split_new[14])

                    if (Marker_lineage != 'root') and (bin_size_Mbp >= 0.5):
                        quality_file_handle_qualified.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (bin_name, Marker_lineage, bin_size_Mbp, completeness, contamination, Heterogeneity))
                    elif (Marker_lineage == 'root') or (bin_size_Mbp < 0.5):
                        quality_file_handle_unploted.write('%s\t%s\t%s\t%s\t%s\t%s\n' % (bin_name, Marker_lineage, bin_size_Mbp, completeness, contamination, Heterogeneity))
                        unploted_bin_number += 1

    quality_file_handle_unploted.close()
    quality_file_handle_qualified.close()

    if unploted_bin_number == 0:
        os.remove(pwd_quality_file_unploted)


# initialize list of list
list_of_bin_folder_name = []
list_of_completeness_list = []
list_of_contamination_list = []
list_of_bin_size_list = []
list_of_bin_number = []
list_of_good_bin_number = []
list_of_contamination_free_bin_number = []
list_of_total_length = []
list_of_good_bin_total_length = []
list_of_contamination_free_bin_total_length = []
list_of_contamination_free_bin_list = []

for each_bin_folder_2 in input_bin_folder_list:
    if '/' in each_bin_folder_2:
        each_bin_folder_2_split = each_bin_folder_2.split('/')
        each_bin_folder_2 = each_bin_folder_2_split[-1]
    list_of_bin_folder_name.append(each_bin_folder_2)
    pwd_bin_quality_file_2 = '%s/outputs/Bin_qualities_%s_qualified.txt' % (wd, each_bin_folder_2)
    bin_qualities = open(pwd_bin_quality_file_2)

    completeness_list = []
    contamination_list = []
    bin_size_list = []
    contamination_free_bin_list = []
    bin_number = 0
    good_bin_number = 0
    contamination_free_bin_number = 0
    total_length = 0
    good_bin_total_length = 0
    contamination_free_bin_total_length = 0

    for each_bin_quality in bin_qualities:
        each_bin_quality_split = each_bin_quality.strip().split('\t')
        if each_bin_quality_split[0] != 'Bin_name':
            bin_size_Mbp_2 = float("{0:.2f}".format(float(each_bin_quality_split[2])))
            completeness_2 = float("{0:.2f}".format(float(each_bin_quality_split[3])))
            contamination_2 = float("{0:.2f}".format(float(each_bin_quality_split[4])))

            bin_size_list.append(bin_size_Mbp_2)
            completeness_list.append(completeness_2)
            contamination_list.append(contamination_2)

            # all bins
            bin_number += 1
            total_length += bin_size_Mbp_2

            # good quality bins
            if (completeness_2 >= 70) and (contamination_2 <= 5):
                good_bin_number += 1
                good_bin_total_length += bin_size_Mbp_2

            # contamination-free bins
            if contamination_2 == 0:
                contamination_free_bin_number += 1
                contamination_free_bin_total_length += bin_size_Mbp_2
                contamination_free_bin_list.append(each_bin_quality_split[0])

    total_length = float("{0:.2f}".format(total_length))
    good_bin_total_length = float("{0:.2f}".format(good_bin_total_length))
    contamination_free_bin_total_length = float("{0:.2f}".format(contamination_free_bin_total_length))

    list_of_completeness_list.append(completeness_list)
    list_of_contamination_list.append(contamination_list)
    list_of_bin_size_list.append(bin_size_list)
    list_of_bin_number.append(bin_number)
    list_of_good_bin_number.append(good_bin_number)
    list_of_contamination_free_bin_number.append(contamination_free_bin_number)
    list_of_total_length.append(total_length)
    list_of_good_bin_total_length.append(good_bin_total_length)
    list_of_contamination_free_bin_total_length.append(contamination_free_bin_total_length)
    list_of_contamination_free_bin_list.append(contamination_free_bin_list)


# turn number list to array
list_of_completeness_list_array =                   list(map(get_array, list_of_completeness_list))
list_of_contamination_list_array =                  list(map(get_array, list_of_contamination_list))
list_of_bin_size_list_array =                       list(map(get_array, list_of_bin_size_list))
list_of_bin_number_array =                          list(map(get_array, list_of_bin_number))
list_of_good_bin_number_array =                     list(map(get_array, list_of_good_bin_number))
list_of_contamination_free_bin_number_array =       list(map(get_array, list_of_contamination_free_bin_number))
list_of_total_length_array =                        list(map(get_array, list_of_total_length))
list_of_good_bin_total_length_array =               list(map(get_array, list_of_good_bin_total_length))
list_of_contamination_free_bin_total_length_array = list(map(get_array, list_of_contamination_free_bin_total_length))


###################################################### Plot Image ######################################################

fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(24, 6))
label_name_list = list_of_bin_folder_name

# box plot of completeness, contamination and bin size
boxplot_inputs = [list_of_completeness_list_array, list_of_contamination_list_array, list_of_bin_size_list_array]
title_list = ['Completeness (CheckM)', 'Contamination (CheckM)', 'Bin Size (Mbp)']

n = 0
for each_plot in boxplot_inputs:
    axes[n].boxplot(boxplot_inputs[n], labels=label_name_list, showfliers=False)
    axes[n].set_title(title_list[n], fontsize=12)
    n += 1

# plot scatter plot for bin number and total length
dots_all_bin = []
dots_good_bin = []
dots_con_free_bin = []
n = 0
axes_num = 3

color_list = []

if len(input_bin_folder_list) == 3:
    color_list = ['red', 'blue', 'green']
if len(input_bin_folder_list) == 4:
    color_list = ['red', 'blue', 'orange', 'green']


for each_bin_set in input_bin_folder_list:
    # dot for all bins
    plot_point_all_bin = axes[axes_num].scatter(list_of_bin_number_array[n],  # get x axis value
                                                list_of_total_length_array[n],  # get y axis value
                                                marker='o', color=color_list[n], s=30)

    # dot for good bins
    plot_point_good_bin = axes[axes_num].scatter(list_of_good_bin_number_array[n],
                                                     list_of_good_bin_total_length_array[n],
                                                     marker='^', color=color_list[n], s=30)

    # dot for contamination free bins
    plot_point_con_free_bin = axes[axes_num].scatter(list_of_contamination_free_bin_number_array[n],
                                                     list_of_contamination_free_bin_total_length_array[n],
                                                     marker='s', color=color_list[n], s=30)
    dots_all_bin.append(plot_point_all_bin)
    dots_good_bin.append(plot_point_good_bin)
    dots_con_free_bin.append(plot_point_con_free_bin)
    n += 1


#add legend to scatter plot
if len(input_bin_folder_list) == 3:
    axes[axes_num].legend((dots_con_free_bin[0],
                           dots_con_free_bin[1],
                           dots_con_free_bin[2],
                           dots_good_bin[0],
                           dots_good_bin[1],
                           dots_good_bin[2],
                           dots_all_bin[0],
                           dots_all_bin[1],
                           dots_all_bin[2]),
                          ('%s_cf' % label_name_list[0][:2],
                           '%s_cf' % label_name_list[1][:2],
                           '%s_cf' % label_name_list[2][:2],
                           '%s_gd' % label_name_list[0][:2],
                           '%s_gd' % label_name_list[1][:2],
                           '%s_gd' % label_name_list[2][:2],
                           '%s_al' % label_name_list[0][:2],
                           '%s_al' % label_name_list[1][:2],
                           '%s_al' % label_name_list[2][:2]),
                          loc='upper center', ncol=3, fontsize=11, scatterpoints=1)


if len(input_bin_folder_list) == 4:
    axes[axes_num].legend((dots_con_free_bin[0],
                           dots_con_free_bin[1],
                           dots_con_free_bin[2],
                           dots_con_free_bin[3],
                           dots_good_bin[0],
                           dots_good_bin[1],
                           dots_good_bin[2],
                           dots_good_bin[3],
                           dots_all_bin[0],
                           dots_all_bin[1],
                           dots_all_bin[2],
                           dots_all_bin[3]),
                          ('%s_cf' % label_name_list[0][:2],
                           '%s_cf' % label_name_list[1][:2],
                           '%s_cf' % label_name_list[2][:2],
                           '%s_cf' % label_name_list[3][:2],
                           '%s_gd' % label_name_list[0][:2],
                           '%s_gd' % label_name_list[1][:2],
                           '%s_gd' % label_name_list[2][:2],
                           '%s_gd' % label_name_list[3][:2],
                           '%s_al' % label_name_list[0][:2],
                           '%s_al' % label_name_list[1][:2],
                           '%s_al' % label_name_list[2][:2],
                           '%s_al' % label_name_list[3][:2]),
                          loc='upper center', ncol=3, fontsize=11, scatterpoints=1)


# add title and x/y axis name to scatter plot
axes[axes_num].set_title('Bin Number and Total Length', fontsize=12)
axes[axes_num].set_xlabel('Bin Number')
axes[axes_num].set_ylabel('Total Length (Mbp)')


# set x/y axis range
x_min = min(list_of_contamination_free_bin_number_array) - min(list_of_bin_number_array) / 5
if x_min < 0:
    x_min = 0

x_max = max(list_of_bin_number_array) + min(list_of_bin_number_array) / 5
y_min = min(list_of_contamination_free_bin_total_length_array) - min(list_of_total_length_array) / 5
if y_min < 0:
    y_min = 0

y_max = max(list_of_total_length_array) + max(list_of_total_length_array) / 3
axes[axes_num].axis([x_min, x_max, y_min, y_max])

fig.subplots_adjust(wspace=0.25)
plt.savefig(pwd_statistics_image, dpi=300, format='png')

