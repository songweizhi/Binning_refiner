import os
import glob
from lib.get_bin_size import get_bin_size

def get_bin_statistics(pwd_checkm_wd, checkm_wd_name, bin_file_extention):
    # get bin name list
    bin_files_re = '%s/*.%s' % (pwd_checkm_wd, bin_file_extention)
    bins = [os.path.basename(file_name) for file_name in glob.glob(bin_files_re)]
    if len(bins) == 0:
        print('No input bin detected from %s, please-check' % pwd_checkm_wd)
        exit()

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
    for each_bin in bins:
        bin_name = each_bin[:-(len(bin_file_extention) + 1)]
        pwd_checkm_output = '%s/%s/%s/out_%s/out_%s.txt' % (pwd_checkm_wd, checkm_wd_name, bin_name, bin_name, bin_name)
        pwd_bin_file = '%s/%s' % (pwd_checkm_wd, each_bin)
        bin_size = get_bin_size(pwd_bin_file)
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

    # transfer length in bp to length in MB
    total_length_mb = total_length_bp/(1024*1024)
    con_free_total_length_mb = con_free_total_length_bp/(1024*1024)
    # return statistics
    return completeness_list, contamination_list, bin_size_list, bin_number, con_free_bin_number, total_length_mb, con_free_total_length_mb, con_free_bin_list

