import os
import glob
import shutil
from lib.plot_bin_quality import plot_bin_quality

###################################### CONFIGURATION ######################################

wd = '/Users/weizhisong/Desktop/new_wd_20/refine_wd/output_MetaBAT_vs_MyCC/refined_bins'
file_extention = 'fasta'
contamination_cutoff = 20

###########################################################################################

# create folder to hold qualified bins
checkm_wd = 'qsub_wd'
checkm_results_summary_folder = '0_CheckM_results_summary'
qualified_bins_folder = 'Qualified_bins_contamination_%s' % contamination_cutoff
qualified_bins_txt = 'Bins_quality_contamination_%s.txt' % contamination_cutoff
all_bins_stat_txt = 'Bins_quality_all.txt'
bin_quality_image_all = 'Bins_quality_all.png'
bin_quality_image_qualified = 'Bins_quality_contamination_%s.png' % contamination_cutoff


pwd_checkm_results_summary_folder = '%s/%s' % (wd, checkm_results_summary_folder)
pwd_qualified_bins_folder = '%s/%s' % (pwd_checkm_results_summary_folder, qualified_bins_folder)
pwd_qualified_bins_txt = '%s/%s' % (pwd_checkm_results_summary_folder, qualified_bins_txt)
pwd_all_bins_stat_txt = '%s/%s' % (pwd_checkm_results_summary_folder, all_bins_stat_txt)
pwd_bin_quality_image = '%s/%s' % (pwd_checkm_results_summary_folder, bin_quality_image_all)
pwd_bin_quality_image_qualified = '%s/%s' % (pwd_checkm_results_summary_folder, bin_quality_image_qualified)

if not os.path.isdir(pwd_checkm_results_summary_folder):
    os.mkdir(pwd_checkm_results_summary_folder)
else:
    shutil.rmtree(pwd_checkm_results_summary_folder)
    os.mkdir(pwd_checkm_results_summary_folder)



if not os.path.isdir(pwd_qualified_bins_folder):
    os.mkdir(pwd_qualified_bins_folder)
else:
    shutil.rmtree(pwd_qualified_bins_folder)
    os.mkdir(pwd_qualified_bins_folder)

# get bin name list
bin_files = '%s/*.%s' % (wd, file_extention)
bins = [os.path.basename(file_name) for file_name in glob.glob(bin_files)]
qualified_bins = open(pwd_qualified_bins_txt, 'w')
all_bins = open(pwd_all_bins_stat_txt, 'w')
qualified_bins.write('Bin_Name\tCompleteness\tContamination\n')
all_bins.write('Bin_Name\tCompleteness\tContamination\n')

for bin in bins:
    bin_folder = bin[:-(len(file_extention) + 1)]
    pwd_checkm_output = '%s/%s/%s/out_%s/out_%s.txt' % (wd, checkm_wd, bin_folder, bin_folder, bin_folder)
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
                bin_name = quality_split_new[0]
                completeness = float(quality_split_new[12])
                contamination = float(quality_split_new[13])
                all_bins.write('%s\t%s\t%s\n' % (bin_name, completeness, contamination))
                if (completeness != 0) and (contamination <= contamination_cutoff):
                    qualified_bins.write('%s\t%s\t%s\n' % (bin_name, completeness, contamination))
                    pwd_bin = '%s/%s' % (wd, bin)
                    os.system('cp %s %s' % (pwd_bin, pwd_qualified_bins_folder))
                else:
                    pass
    else:
        all_bins.write('%s\tNo CheckM outputs detected\n' % bin_folder)
qualified_bins.close()
all_bins.close()


# plot all bins' quality
plot_bin_quality(pwd_all_bins_stat_txt, bin_quality_image_all.split('.')[0], pwd_bin_quality_image)

# plot qualified bins' quality
plot_bin_quality(pwd_qualified_bins_txt, bin_quality_image_qualified.split('.')[0], pwd_bin_quality_image_qualified)
