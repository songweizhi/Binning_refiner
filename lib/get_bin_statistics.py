import os
import glob
from lib.get_bin_size import get_bin_size

def get_bin_statistics(bin_folder, checkm_wd_name, out):
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
    qualities_all_bins_filename = '%s_bins_qualities.txt' % bin_folder_name
    pwd_qualities_all_bins_filename = '%s/%s' % (out, qualities_all_bins_filename)
    qualities_all_bins = open(pwd_qualities_all_bins_filename, 'w')
    qualities_all_bins.write('Bin_name\tBin_size(MB)\tCompleteness\tContamination\n')
    for each_bin in bins:
        bin_name = each_bin[:-(len(bin_file_extension) + 1)]
        pwd_checkm_output = '%s/%s/%s.txt' % (bin_folder, checkm_wd_name, bin_name)

        # check whether CheckM results exist
        if not os.path.exists('%s/%s' % (bin_folder, checkm_wd_name)):
            print('No CheckM results detected from %s, please double-check.' % bin_folder)
            exit()
        else:
            pass

        pwd_bin_file = '%s/%s' % (bin_folder, each_bin)
        bin_size = get_bin_size(pwd_bin_file)
        bin_size_MB = float("{0:.2f}".format(bin_size/(1024*1024)))
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

