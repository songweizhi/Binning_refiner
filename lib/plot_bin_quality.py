import numpy as np
import matplotlib.pyplot as plt

def plot_bin_quality(bin_quality_file, image_title, pwd_image_file):

    # get lists of bin_name, completeness and contamination
    all_bins_stat = open(bin_quality_file)
    bin_name_list = []
    completeness_list = []
    contamination_list = []
    for each_line in all_bins_stat:
        if not each_line.startswith('Bin_Name'):
            each_line_split = each_line.strip().split('\t')
            if each_line_split[1] == 'No CheckM outputs detected':
                pass
            else:
                bin_name = each_line_split[0]
                completeness = float(each_line_split[1])
                contamination = float(each_line_split[2])
                bin_name_list.append(bin_name)
                completeness_list.append(completeness)
                contamination_list.append(contamination)

    # Add bin number to image title
    image_title = '%s(%s)' % (image_title, len(bin_name_list))

    # plot image
    N = len(bin_name_list)
    ind = np.arange(N)  # the x locations for the groups
    width = 0.5
    fig, ax = plt.subplots()
    completeness_plot = ax.bar(ind, completeness_list, width, color= 'blue', edgecolor = 'none')  # completeness bar
    contamination_plot = ax.bar(ind, contamination_list, width, color= 'red', edgecolor = 'none')  # contamination bar
    ax.set_ylabel('CheckM Scores')  # set Y axis name
    ax.set_title(image_title)  # set image title
    ax.set_xticks(ind + width)
    ax.set_xticklabels(bin_name_list, rotation=90, size = 6)
    ax.legend((completeness_plot[0], contamination_plot[0]), ('Completeness', 'Contamination'), fontsize = 10)  # set legend
    # export image
    plt.savefig(pwd_image_file, dpi = 300, format = 'png')
