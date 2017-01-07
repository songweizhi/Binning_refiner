import os
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
                    help='path to 1st bin folder',
                    required=True)

parser.add_argument('-2',
                    help='path to 2nd bin folder',
                    required=True)

parser.add_argument('-r',
                    help='path to refined bin folder',
                    required=True)

parser.add_argument('-ms',
                    required=False,
                    default=524288,
                    type=int,
                    help='(optional) minimum size for refined bins, default = 524288 (0.5MB)')

args = vars(parser.parse_args())

if args['1'][-1] == '/':
    args['1'] = args['1'][:-1]
if args['2'][-1] == '/':
    args['2'] = args['2'][:-1]
if args['r'][-1] == '/':
    args['r'] = args['r'][:-1]

bin_size_cutoff = int(args['ms'])
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

def get_bin_statistics(bin_folder, checkm_wd_name, out, bin_size_cutoff):
    # get bin name list
    bin_folder_name = bin_folder.split('/')[-1]

    bin_files_re = '%s/*.fa*' % (bin_folder)
    bins = [os.path.basename(file_name) for file_name in glob.glob(bin_files_re)]
    if len(bins) == 0:
        print('No input bin detected from %s, please double-check.' % bin_folder)
        exit()

    bin_file_ext_list = []
    for bin in bins:
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
              'for each bin sets.' % bin_folder)
        exit()
    else:
        pass

    # get bin file extension
    bin_file_extension = bin_file_ext_list_uniq[0]

    # initialize output
    completeness_list = []
    contamination_list = []
    bin_size_list = []
    bin_number = 0
    con_free_bin_number = 0
    con_free_bin_list = []
    total_length_bp = 0
    con_free_total_length_bp = 0
    # get statistics
    qualities_all_bins_filename = 'Bin_qualities_%s.txt' % bin_folder_name
    pwd_qualities_all_bins_filename = '%s/%s' % (out, qualities_all_bins_filename)
    qualities_all_bins = open(pwd_qualities_all_bins_filename, 'w')
    qualities_all_bins.write('Bin_name\tBin_size(Mbp)\tCompleteness\tContamination\n')
    for each_bin in bins:
        bin_name = each_bin[:-(len(bin_file_extension) + 1)]
        pwd_checkm_output = '%s/%s/%s.txt' % (bin_folder, checkm_wd_name, bin_name)

        # check whether CheckM results exist
        if not os.path.exists('%s/%s' % (bin_folder, checkm_wd_name)):
            print('No CheckM results detected from %s, please run CkeckM_qsuber.py for this bin set first.' % bin_folder)
            exit()
        else:
            pass

        pwd_bin_file = '%s/%s' % (bin_folder, each_bin)
        bin_size = get_bin_size(pwd_bin_file)
        bin_size_MB = float("{0:.2f}".format(bin_size/(1024*1024)))

        if bin_size >= bin_size_cutoff:
            bin_size_list.append(bin_size / (1024 * 1024))
            total_length_bp += bin_size
            bin_number += 1
            if os.path.exists(pwd_checkm_output):
                qualities = open(pwd_checkm_output)
                for quality in qualities:
                    if (quality.startswith('--')) or (quality.startswith('  Bin Id')):
                        pass
                    else:
                        quality_split = quality.strip().split(' ')
                        quality_split_new = []
                        for each in quality_split:
                            if each != '':
                                quality_split_new.append(each)

                        completeness = float(quality_split_new[12])
                        contamination = float(quality_split_new[13])
                        completeness_list.append(completeness)
                        contamination_list.append(contamination)
                        if contamination == 0:
                            con_free_bin_number += 1
                            con_free_bin_list.append(each_bin)
                            con_free_total_length_bp += bin_size

                        qualities_all_bins.write('%s\t%s\t%s\t%s\n' % (bin_name, bin_size_MB, completeness, contamination))

    # transfer length in bp to length in MB
    total_length_mb = total_length_bp/(1024*1024)
    con_free_total_length_mb = con_free_total_length_bp/(1024*1024)
    # return statistics
    qualities_all_bins.close()
    return completeness_list, contamination_list, bin_size_list, bin_number, con_free_bin_number, total_length_mb, con_free_total_length_mb, con_free_bin_list


def plot_identity_list(identity_list, identity_cut_off, title, output_foler):

    # get total length
    total_size = float("{0:.2f}".format(sum(identity_list)/(1024*1024)))
    identity_cut_off = identity_cut_off/(1024*1024)
    identity_cut_off = float("{0:.2f}".format(identity_cut_off))

    identity_list_MB = []
    for size in identity_list:
        size_in_MB = size/(1024*1024)
        size_in_MB = float("{0:.3f}".format(size_in_MB))
        identity_list_MB.append(size_in_MB)

    # get statistics
    match_number = len(identity_list_MB)
    average_size = float(np.average(identity_list_MB))
    average_size = float("{0:.2f}".format(average_size))
    max_match = float(np.max(identity_list_MB))
    min_match = float(np.min(identity_list_MB))
    # get hist plot
    num_bins = 50
    plt.hist(identity_list_MB,
             num_bins,
             alpha = 0.1,
             facecolor = 'blue')
    plt.title(title)
    plt.xlabel('Size (MB)')
    plt.ylabel('Number')
    plt.subplots_adjust(left = 0.15)
    # add text
    x_min = plt.xlim()[0]  # get the x-axes minimum value
    x_max = plt.xlim()[1]  # get the x-axes maximum value
    y_min = plt.ylim()[0]  # get the y-axes minimum value
    y_max = plt.ylim()[1]  # get the y-axes maximum value
    # set text position
    text_x = x_min + (x_max - x_min)/5 * 3.5
    text_y_total = y_min + (y_max - y_min) / 5 * 4.4
    text_y_min = y_min + (y_max - y_min) / 5 * 4.1
    text_y_max = y_min + (y_max - y_min) / 5 * 3.8
    text_y_average = y_min + (y_max - y_min) / 5 * 3.5
    text_y_cutoff = y_min + (y_max - y_min) / 5 * 3.2
    text_y_sum = y_min + (y_max - y_min) / 5 * 2.9

    # plot text
    plt.text(text_x, text_y_total, 'Total: %s' % match_number)
    plt.text(text_x, text_y_min, 'Min: %s' % min_match)
    plt.text(text_x, text_y_max, 'Max: %s' % max_match)
    plt.text(text_x, text_y_average, 'Mean: %s' % average_size)
    plt.text(text_x, text_y_cutoff, 'Cutoff: %s' % identity_cut_off)
    plt.text(text_x, text_y_sum, 'Total length: %s' % total_size)

    plt.annotate(' ',
            xy = (identity_cut_off, 0),
            xytext = (identity_cut_off, (y_max - y_min)/10),
            arrowprops = dict(width = 0.5,
                              headwidth = 0.5,
                              facecolor = 'red',
                              edgecolor = 'red',
                              shrink = 0.02))
    # Get plot
    plt.savefig('%s/%s.png' % (output_foler, title), dpi = 300)
    plt.close()



def get_bin_size(bin_file):
    bin_content = SeqIO.parse(bin_file, 'fasta')
    total_length = 0
    for each in bin_content:
        contig_length = len(each.seq)
        total_length += contig_length
    return total_length



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
    total_length, contamination_free_bin_total_length, contamination_free_bin_list = get_bin_statistics(bin_folder, checkm_wd_name, out, bin_size_cutoff)

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
title_list = ['Completeness (CheckM)', 'Contamination (CheckM)', 'Bin Size (Mbp)']
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
axes[axes_num].set_ylabel('Total Length (Mbp)')

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

