import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

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
