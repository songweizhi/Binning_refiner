import os
import shutil
import argparse
import numpy as np
from scipy import stats
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from lib.get_array import get_array
from lib.get_bin_statistics import get_bin_statistics

#################################################### CONFIGURATION #####################################################

parser = argparse.ArgumentParser()

parser.add_argument('-1',
                    help='path to 1st bin folder',
                    required=True)

parser.add_argument('-2',
                    help='path to 2nd bin folder',
                    required=True)

parser.add_argument('-r',
                    help='path to refined bin folder',
                    required=True)

args = vars(parser.parse_args())

if args['1'][-1] == '/':
    args['1'] = args['1'][:-1]
if args['2'][-1] == '/':
    args['2'] = args['2'][:-1]
if args['r'][-1] == '/':
    args['r'] = args['r'][:-1]

bin_folders = [args['1'], args['2'], args['r']]

########################################################################################################################

# define folder/file name
out = os.getcwd()
checkm_wd_name = 'checkm_wd'
contamination_free_refined_bin_folder = 'contamination_free_refined_bins'
statistics_txt_filename = 'Bin_qualities_overall.txt'
statistics_image_filename = 'Bin_qualities_overall.png'
pwd_statistics_txt = '%s/%s' % (out, statistics_txt_filename)
pwd_statistics_image = '%s/%s' % (out, statistics_image_filename)
pwd_contamination_free_refined_bin_folder = '%s/%s' % (args['r'], contamination_free_refined_bin_folder)

#################################################### Get input data ####################################################

# initialize list of list
list_of_completeness_list = []
list_of_contamination_list = []
list_of_bin_size_list = []
list_of_qualified_bin_number = []
list_of_contamination_free_bin_number = []
list_of_total_length = []
list_of_contamination_free_bin_total_length = []
list_of_contamination_free_bin_list = []

for bin_folder in bin_folders:
    completeness_list, contamination_list, bin_size_list, qualified_bin_number, contamination_free_bin_number, \
    total_length, contamination_free_bin_total_length, contamination_free_bin_list = get_bin_statistics(bin_folder, checkm_wd_name, out)

    list_of_completeness_list.append(completeness_list)
    list_of_contamination_list.append(contamination_list)
    list_of_bin_size_list.append(bin_size_list)
    list_of_qualified_bin_number.append(qualified_bin_number)
    list_of_contamination_free_bin_number.append(contamination_free_bin_number)
    list_of_total_length.append(total_length)
    list_of_contamination_free_bin_total_length.append(contamination_free_bin_total_length)
    list_of_contamination_free_bin_list.append(contamination_free_bin_list)


# get basic statistics of first bin set
statistics_overall_out = open(pwd_statistics_txt, 'w')
statistics_overall_out.write('\t\t\t%s\t%s\t%s\n'               % (args['1'].split('/')[-1], args['2'].split('/')[-1], args['r'].split('/')[-1]))
statistics_overall_out.write('Bin number\t\t%s\t%s\t%s\n'       % (len(list_of_contamination_list[0]), len(list_of_contamination_list[1]), len(list_of_contamination_list[2])))
statistics_overall_out.write('Completeness Mean\t%s\t%s\t%s\n'  % (float("{0:.2f}".format(np.mean(list_of_completeness_list[0]))), float("{0:.2f}".format(np.mean(list_of_completeness_list[1]))), float("{0:.2f}".format(np.mean(list_of_completeness_list[2])))))
statistics_overall_out.write('Completeness Std\t%s\t%s\t%s\n'   % (float("{0:.2f}".format(np.std(list_of_completeness_list[0]))), float("{0:.2f}".format(np.std(list_of_completeness_list[1]))), float("{0:.2f}".format(np.std(list_of_completeness_list[2])))))
statistics_overall_out.write('Contamination Mean\t%s\t%s\t%s\n' % (float("{0:.2f}".format(np.mean(list_of_contamination_list[0]))), float("{0:.2f}".format(np.mean(list_of_contamination_list[1]))), float("{0:.2f}".format(np.mean(list_of_contamination_list[2])))))
statistics_overall_out.write('Contamination Std\t%s\t%s\t%s\n'  % (float("{0:.2f}".format(np.std(list_of_contamination_list[0]))), float("{0:.2f}".format(np.std(list_of_contamination_list[1]))), float("{0:.2f}".format(np.std(list_of_contamination_list[2])))))
statistics_overall_out.write('Bin size Mean\t\t%s\t%s\t%s\n'    % (float("{0:.2f}".format(np.mean(list_of_bin_size_list[0]))), float("{0:.2f}".format(np.mean(list_of_bin_size_list[1]))), float("{0:.2f}".format(np.mean(list_of_bin_size_list[2])))))
statistics_overall_out.write('Bin size Std\t\t%s\t%s\t%s\n'     % (float("{0:.2f}".format(np.std(list_of_bin_size_list[0]))), float("{0:.2f}".format(np.std(list_of_bin_size_list[1]))), float("{0:.2f}".format(np.std(list_of_bin_size_list[2])))))
statistics_overall_out.write('\n\nP-value(Two-sample t-test):\n\t%s_vs_%s\t%s_vs_%s\n' % (args['1'].split('/')[-1], args['r'].split('/')[-1], args['2'].split('/')[-1], args['r'].split('/')[-1]))
statistics_overall_out.write('Completeness\t%s\t%s\n'           % (float("{0:.3f}".format(stats.ttest_ind(list_of_completeness_list[0], list_of_completeness_list[2], equal_var=False).pvalue)), float("{0:.3f}".format(stats.ttest_ind(list_of_completeness_list[1], list_of_completeness_list[2], equal_var=False).pvalue))))
statistics_overall_out.write('Contamination\t%s\t%s\n'          % (float("{0:.3f}".format(stats.ttest_ind(list_of_contamination_list[0], list_of_contamination_list[2], equal_var=False).pvalue)), float("{0:.3f}".format(stats.ttest_ind(list_of_contamination_list[1], list_of_contamination_list[2], equal_var=False).pvalue))))
statistics_overall_out.write('Bin size\t%s\t%s\n'               % (float("{0:.3f}".format(stats.ttest_ind(list_of_bin_size_list[0], list_of_bin_size_list[2], equal_var=False).pvalue)), float("{0:.3f}".format(stats.ttest_ind(list_of_bin_size_list[1], list_of_bin_size_list[2], equal_var=False).pvalue))))
statistics_overall_out.close()

# turn number list to array
list_of_completeness_list_array =                   list(map(get_array, list_of_completeness_list))
list_of_contamination_list_array =                  list(map(get_array, list_of_contamination_list))
list_of_bin_size_list_array =                       list(map(get_array, list_of_bin_size_list))
list_of_qualified_bin_number_array =                list(map(get_array, list_of_qualified_bin_number))
list_of_contamination_free_bin_number_array =       list(map(get_array, list_of_contamination_free_bin_number))
list_of_total_length_array =                        list(map(get_array, list_of_total_length))
list_of_contamination_free_bin_total_length_array = list(map(get_array, list_of_contamination_free_bin_total_length))

###################################################### Plot Image ######################################################

fig, axes = plt.subplots(nrows=1, ncols=4, figsize=(24, 6))
label_name_list = [bin_folders[0].split('/')[-1], bin_folders[1].split('/')[-1], bin_folders[2].split('/')[-1]]

# box plot of completeness, contamination and bin size
boxplot_inputs = [list_of_completeness_list_array, list_of_contamination_list_array, list_of_bin_size_list_array]
title_list = ['Completeness (CheckM)', 'Contamination (CheckM)', 'Bin Size (MB)']
n = 0
for each_plot in boxplot_inputs:
    axes[n].boxplot(boxplot_inputs[n], labels=label_name_list, showfliers=False)
    axes[n].set_title(title_list[n], fontsize=12)
    n += 1

# scatter plot for bin number and total length
dots_all_bin = []
dots_con_free_bin = []
n = 0
axes_num = 3
color_list = ['red', 'blue', 'green']

for each_bin_set in bin_folders:
    # dot for all bins
    plot_point_all_bin = axes[axes_num].scatter(list_of_qualified_bin_number_array[n],  # get x axis value
                                                list_of_total_length_array[n],  # get y axis value
                                                marker='o', color=color_list[n], s=30)
    # dot for contamination free bins
    plot_point_con_free_bin = axes[axes_num].scatter(list_of_contamination_free_bin_number_array[n],
                                                     list_of_contamination_free_bin_total_length_array[n],
                                                     marker='s', color=color_list[n], s=30)
    dots_all_bin.append(plot_point_all_bin)
    dots_con_free_bin.append(plot_point_con_free_bin)
    n += 1

# add legend to scatter plot
axes[axes_num].legend((dots_con_free_bin[0],
                       dots_con_free_bin[1],
                       dots_con_free_bin[2],
                       dots_all_bin[0],
                       dots_all_bin[1],
                       dots_all_bin[2]),
                      ('%s_con_free' % label_name_list[0],
                       '%s_con_free' % label_name_list[1],
                       '%s_con_free' % label_name_list[2],
                       '%s_all' % label_name_list[0],
                       '%s_all' % label_name_list[1],
                       '%s_all' % label_name_list[2]),
                      loc='upper right', ncol=2, fontsize=11, scatterpoints=1)

# add title and x/y axis name to scatter plot
axes[axes_num].set_title('Bin Number and Total Length', fontsize=12)
axes[axes_num].set_xlabel('Bin Number')
axes[axes_num].set_ylabel('Total Length (MB)')

# set x/y axis range
x_min = min(list_of_contamination_free_bin_number_array) - min(list_of_qualified_bin_number_array) / 5
if x_min < 0:
    x_min = 0

x_max = max(list_of_qualified_bin_number_array) + min(list_of_qualified_bin_number_array) / 5
y_min = min(list_of_contamination_free_bin_total_length_array) - min(list_of_total_length_array) / 5
if y_min < 0:
    y_min = 0

y_max = max(list_of_total_length_array) + max(list_of_total_length_array) / 4
axes[axes_num].axis([x_min, x_max, y_min, y_max])

fig.subplots_adjust(wspace=0.25)
plt.savefig(pwd_statistics_image, dpi=300, format='png')


# get bins blow defined contamination cutoff
# create folder to hold contamination free refined bins
if not os.path.isdir(pwd_contamination_free_refined_bin_folder):
    os.mkdir(pwd_contamination_free_refined_bin_folder)
else:
    shutil.rmtree(pwd_contamination_free_refined_bin_folder)
    os.mkdir(pwd_contamination_free_refined_bin_folder)

# copy contamination free refined bins to defined bin folder
contamination_free_refined_bins = list_of_contamination_free_bin_list[2]
for contamination_free_refined_bin in contamination_free_refined_bins:
    pwd_contamination_free_refined_bin = '%s/%s' % (args['r'], contamination_free_refined_bin)
    os.system('cp %s %s' % (pwd_contamination_free_refined_bin, pwd_contamination_free_refined_bin_folder))

