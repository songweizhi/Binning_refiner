import os
import glob
import shutil
import argparse

"""

    It will:
    1. Create a new folder for each of your input bins and copy your bin into its corresponding folder
    2. Generate qsub file to run CheckM for each input bin
    3. Submit generated qsub files

"""

#################################################### CONFIGURATION #####################################################

parser = argparse.ArgumentParser()

parser.add_argument('-email',
                    required=True,
                    help='your email address',
                    metavar='(req)')

parser.add_argument('-nodes',
                    required=False,
                    default=1,
                    type=int,
                    help='nodes number needed (default = 1)',
                    metavar='(opt)')

parser.add_argument('-ppn',
                    required=False,
                    default=12,
                    type=int,
                    help='ppn number needed (default = 12)',
                    metavar='(opt)')

parser.add_argument('-memory',
                    required=False,
                    default=120,
                    type=int,
                    help='memory needed (default = 120)',
                    metavar='(opt)')

parser.add_argument('-walltime',
                    required=False,
                    default='2:59:00',
                    help='walltime needed (default = 2:59:00)',
                    metavar='(opt)')

parser.add_argument('-python',
                    required=False,
                    default='python/2.7.8',
                    help='python version (default: python/2.7.8)',
                    metavar='(opt)')

parser.add_argument('-hmmer',
                    required=False,
                    default='hmmer/3.1b2',
                    help='hmmer version (default: hmmer/3.1b2)',
                    metavar='(opt)')

parser.add_argument('-pplacer',
                    required=False,
                    default='pplacer/1.1.alpha16',
                    help='pplacer version (default: pplacer/1.1.alpha16)',
                    metavar='(opt)')

parser.add_argument('-prodigal',
                    required=False,
                    default='prodigal/2.6.3',
                    help='prodigal version (default: prodigal/2.6.3)',
                    metavar='(opt)')

args = parser.parse_args()

wd = os.getcwd()
nodes_number = args.nodes
ppn_number = args.ppn
memory = args.memory
walltime_needed = args.walltime
email = args.email
modules_needed = [args.python, args.hmmer, args.pplacer, args.prodigal]

########################################################################################################################

# define folder/file name
checkm_wd = 'checkm_wd'
qsub_files_folder = 'qsub_files_for_checkm'
pwd_checkm_wd = '%s/%s' % (wd, checkm_wd)
pwd_qsub_files_folder = '%s/%s' % (wd, qsub_files_folder)


# prepare qsub file header
line_1 = '#!/bin/bash\n'
line_2 = '#PBS -l nodes=' + str(nodes_number) + ':ppn=' + str(ppn_number) + '\n'
line_3 = '#PBS -l vmem=' + str(memory) + 'gb\n'
line_4 = '#PBS -l walltime=' + walltime_needed + '\n'
line_5 = '#PBS -j oe\n'
line_6 = '#PBS -M ' + email + '\n'
line_7 = '#PBS -m ae\n'
line_8 = 'cd $PBS_O_WORDIR\n'
#line_8 = 'cd %s\n' % pwd_qsub_files_folder

header = line_1 + line_2 + line_3 + line_4 + line_5 + line_6 + line_7 + line_8

# Prepare module lines
module_lines = ''
for module in modules_needed:
    module_lines += 'module load ' + module + '\n'


def run_qsuber():
    # get bin name list
    bin_files = '%s/*.fa*' % wd
    bins = [os.path.basename(file_name) for file_name in glob.glob(bin_files)]

    if len(bins) == 0:
        print('No input bin detected from %s, please double-check.' % pwd_checkm_wd)
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
              'for all bins in same bin sets.' % pwd_checkm_wd)
        exit()
    else:
        pass

    # get bin file extension
    bin_file_extension = bin_file_ext_list_uniq[0]

    # get qsub file and submit it
    checkm_cmd_file_name = 'Commands_for_CheckM.txt'
    pwd_checkm_cmd_file = '%s/%s' % (pwd_qsub_files_folder, checkm_cmd_file_name)
    checkm_cmd_file = open(pwd_checkm_cmd_file, 'w')
    for bin in bins:
        bin_name = bin[:-(len(bin_file_extension) + 1)]
        qsub_file = '%s.sh' % bin_name
        pwd_qsub_file = '%s/%s' % (pwd_qsub_files_folder, qsub_file)
        out = open(pwd_qsub_file, 'w')
        # create a folder for current bin
        os.mkdir('%s/%s/%s' % (wd, checkm_wd, bin_name))
        pwd_bin = '%s/%s' % (wd, bin)

        pwd_bin_foler = '%s/%s/%s' % (wd, checkm_wd, bin_name)
        os.system('cp %s %s' % (pwd_bin, pwd_bin_foler))
        out.write('%s\n%s' % (header, module_lines))
        cmds = 'checkm lineage_wf -x %s -t %s %s %s -f %s/%s.txt\n' % (
            bin_file_extension, ppn_number, pwd_bin_foler, pwd_bin_foler, pwd_checkm_wd, bin_name)
        cmds_non_qsub = 'checkm lineage_wf -x %s -t %s %s %s -f %s/%s.txt &\n' % (
            bin_file_extension, ppn_number, pwd_bin_foler, pwd_bin_foler, pwd_checkm_wd, bin_name)
        checkm_cmd_file.write(cmds_non_qsub)
        out.write(cmds)
        out.close()
        os.chdir(pwd_qsub_files_folder)
        os.system('qsub %s' % pwd_qsub_file)
        os.chdir(wd)
    checkm_cmd_file.close()


# check whether previous results exist
if os.path.isdir(pwd_checkm_wd):
    choice = str(input('CheckM working directory detected, Press "S/s" to skip this step, Press any other key to overwrite it.\nYour choice: '))
    if choice in ['s', 'S']:
        pass
    else:
        shutil.rmtree(pwd_checkm_wd)
        shutil.rmtree(pwd_qsub_files_folder)
        os.mkdir(pwd_checkm_wd)
        os.mkdir(pwd_qsub_files_folder)
        run_qsuber()
else:
    os.mkdir(pwd_checkm_wd)
    os.mkdir(pwd_qsub_files_folder)
    run_qsuber()
