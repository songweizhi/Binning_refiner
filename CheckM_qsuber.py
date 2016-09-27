import os
import glob
import shutil
import argparse

usage = """

    Usage:

    python3 path/to/this/script.py

    It will:
    1. Create a new folder for each of your input bins and copy your bin into its corresponding folder
    2. Generate qsub file to run CheckM for each input bin
    3. Submit generated qsub files
    4. Bin file extension need to be 'fa', 'fas' or 'fasta'

"""

#################################################### CONFIGURATION #####################################################

parser = argparse.ArgumentParser()

parser.add_argument('-wd',
                    required=True,
                    help='path to working directory',
                    metavar='(required)')

parser.add_argument('-bx',
                    required=True,
                    help='bin file extension',
                    metavar='(required)')

parser.add_argument('-email',
                    required=True,
                    help='your email address',
                    metavar='(required)')

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

parser.add_argument('-python_v',
                    required=False,
                    default='python/2.7.8',
                    help='python version (default: python/2.7.8)',
                    metavar='(opt)')

parser.add_argument('-hmmer_v',
                    required=False,
                    default='hmmer/3.1b2',
                    help='hmmer version (default: hmmer/3.1b2)',
                    metavar='(opt)')

parser.add_argument('-pplacer_v',
                    required=False,
                    default='pplacer/1.1.alpha16',
                    help='pplacer version (default: pplacer/1.1.alpha16)',
                    metavar='(opt)')

parser.add_argument('-prodigal_v',
                    required=False,
                    default='prodigal/2.6.3',
                    help='prodigal version (default: prodigal/2.6.3)',
                    metavar='(opt)')

args = parser.parse_args()

wd = args.wd
bin_file_extention = args.bx
nodes_number = args.nodes
ppn_number = args.ppn
memory = args.memory
walltime_needed = args.walltime
email = args.email
modules_needed = [args.python_v, args.hmmer_v, args.pplacer_v, args.prodigal_v]

########################################################################################################################


# define folder/file name
checkm_wd = 'checkm_wd'
qsub_files_folder = 'qsub_files_for_checkm'
pwd_checkm_wd = '%s/%s' % (wd, checkm_wd)
pwd_qsub_files_folder = '%s/%s' % (wd, qsub_files_folder)


# forward to working directory
os.chdir(wd)

if os.path.isdir(pwd_checkm_wd):
    choice = str(input(
        'CheckM working directory detected, Press "S/s" to skip this step, Press any other key to overwrite it.\nYour choice: '))
    if choice in ['s', 'S']:
        pass
    else:
        pass

########
# put in def
# detected results , not only wd
########


if not os.path.isdir(pwd_checkm_wd):
    os.mkdir(pwd_checkm_wd)
    os.mkdir(pwd_qsub_files_folder)
else:
    shutil.rmtree(pwd_checkm_wd)
    os.mkdir(pwd_checkm_wd)
    os.mkdir(pwd_qsub_files_folder)


# get bin name list
bin_files = '%s/*.fa*' % wd
bins = [os.path.basename(file_name) for file_name in glob.glob(bin_files)]


# prepare qsub file header
line_1 = '#!/bin/bash\n'
line_2 = '#PBS -l nodes=' + str(nodes_number) + ':ppn=' + str(ppn_number) + '\n'
line_3 = '#PBS -l vmem=' + str(memory) + 'gb\n'
line_4 = '#PBS -l walltime=' + walltime_needed + '\n'
line_5 = '#PBS -j oe\n'
line_6 = '#PBS -M ' + email + '\n'
line_7 = '#PBS -m ae\n'
line_8 = 'cd $PBS_O_WORDIR\n'
header = line_1 + line_2 + line_3 + line_4 + line_5 + line_6 + line_7 + line_8
# Prepare module lines
module_lines = ''
for module in modules_needed:
    module_lines += 'module load ' + module + '\n'

# get qsub file and submit it
for bin in bins:
    bin_folder = bin[:-(len(bin_file_extention) + 1)]
    qsub_file = '%s.sh' % bin_folder
    pwd_qsub_file = '%s/%s' % (pwd_qsub_files_folder, qsub_file)
    out = open(pwd_qsub_file, 'w')
    # create a folder for current bin
    os.mkdir('%s/%s/%s' % (wd, checkm_wd, bin_folder))
    pwd_bin = '%s/%s' % (wd, bin)
    pwd_bin_foler = '%s/%s/%s' % (wd, checkm_wd, bin_folder)
    os.system('cp %s %s' % (pwd_bin, pwd_bin_foler))
    out.write('%s\n%s' % (header, module_lines))
    cmds = 'checkm lineage_wf -x %s -t %s %s %s/out_%s -f %s/out_%s/out_%s.txt' % (bin_file_extention, ppn_number, pwd_bin_foler, pwd_bin_foler, bin_folder, pwd_bin_foler, bin_folder, bin_folder)
    out.write(cmds)
    out.close()
    os.system('qsub %s' % pwd_qsub_file)
    #print('qsub %s' % pwd_qsub_file)
