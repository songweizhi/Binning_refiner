#!/usr/bin/env Rscript

# Copyright (C) 2017, Weizhi Song and Torsten Thomas.
# songwz03@gmail.com

# Binning_refiner is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# Binning_refiner is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

suppressMessages(suppressWarnings(library(seqinr)))     # fasta file parser in R
suppressMessages(suppressWarnings(library(assertr)))    # col_concat() funchtion: Concatenate all columns of each row in data frame
suppressMessages(suppressWarnings(library(tidyr)))      # separate() funtion: Separate One Column Into Multiple Columns
suppressMessages(suppressWarnings(library(tools)))      # file_ext() function: Manipulate Filename Extensions
suppressMessages(suppressWarnings(library(optparse)))   # argument parser
suppressMessages(suppressWarnings(library(googleVis)))  # Sankey plot


# example commands
# Rscript /Users/songweizhi/R_scripts/Binning_refiner.R -i input_bin_folder -p TEST


####################################### argument parser ######################################

option_list = list(
  make_option(c("-i", "--infolder"), type="character",    default=NULL,      help="input bin folder"),
  make_option(c("-p", "--prefix"),   type="character",    default='Refined', help="output prefix"),
  make_option(c("-m", "--min"),      type="double",       default=512,       help="minimal size of refined bin"),
  make_option(c("-x", "--width"),    type="double",       default=NULL,      help="the width of sankey plot"),
  make_option(c("-y", "--height"),   type="double",       default=NULL,      help="the height of sankey plot"),
  make_option(c("-q", "--quiet"),    action='store_true', default=FALSE,     help="silent progress report")); 

opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);

input_bin_folder =  opt$infolder
output_bin_prefix = opt$prefix
minBin_size_Kbp =   opt$min
sankey_width =      opt$width
sankey_height =     opt$height
keep_quiet =        opt$quiet


################################### define output filename ###################################

Binning_refiner_wd =              paste(output_bin_prefix, '_', 'Binning_refiner_outputs', sep = '')

report_file_sources_and_length =  paste(Binning_refiner_wd, '/', output_bin_prefix, '_', 'sources_and_length.txt', sep = '')
report_file_contigs =             paste(Binning_refiner_wd, '/', output_bin_prefix, '_', 'contigs.txt', sep = '')
report_file_for_sankey =          paste(Binning_refiner_wd, '/', output_bin_prefix, '_', 'sankey.csv', sep = '')
plot_file_for_sankey =            paste(Binning_refiner_wd, '/', output_bin_prefix, '_', 'sankey.html', sep = '')
output_bin_folder_name =          paste(Binning_refiner_wd, '/', output_bin_prefix, '_', "refined_bins", sep='')


################################### precheck of input files ##################################

# get input_bin_subfolders
input_bin_subfolders = list.dirs(input_bin_folder, recursive=FALSE, full.names = FALSE)

for (bin_subfolder in input_bin_subfolders){
  
  # get bin file list in each input bin subfolder
  pwd_bin_subfolder = paste(input_bin_folder, bin_subfolder, sep = '/')
  bin_file_list = list.files(pwd_bin_subfolder)

  bin_ext_list = c()
  for (each_bin in bin_file_list){
    each_bin_ext = file_ext(each_bin)
    bin_ext_list = c(bin_ext_list, each_bin_ext)
  }
  
  # uniq element
  if (length(unique(bin_ext_list)) > 1){
    message(paste(Sys.time(), 'Program exited, please make sure all bins within', bin_subfolder, 'folder have the same extension'))
    quit()
  }
}

################################# refinement df manipulation #################################

# progress report
if (keep_quiet == FALSE){
  message(paste(Sys.time(), 'Detected', length(input_bin_subfolders), 'input bin folders'))
  }

# initialize contig to bin dataframe
ctg_to_bin_df <- data.frame(matrix(ncol = length(input_bin_subfolders), nrow = 0))
colnames(ctg_to_bin_df)  = input_bin_subfolders

# initialize contig to length dataframe
ctg_to_length_df <- data.frame(matrix(ncol = 1, nrow = 0))
colnames(ctg_to_length_df)  = 'Ctg_length'

# read in contig to bin information
for (bin_subfolder in input_bin_subfolders){
  
  # get bin file list in each input bin subfolder
  pwd_bin_subfolder = paste(input_bin_folder, bin_subfolder, sep = '/')
  bin_file_list = list.files(pwd_bin_subfolder)
  
  # progress report
  if (keep_quiet == FALSE){
    message(paste(Sys.time(), 'Read in', length(bin_file_list), bin_subfolder, 'bins'))
    }
  
  for (each_bin in bin_file_list){
    
    # get path to each bin
    pwd_each_bin = paste(pwd_bin_subfolder, each_bin, sep = '/')
    
    for (each_seq in read.fasta(file = pwd_each_bin, seqtype = 'DNA', as.string = 1, forceDNAtolower = 0)){
      
      # get sequence id and length
      each_seq_id = getName(each_seq)
      each_seq_sequence = getSequence(each_seq)
      each_seq_sequence_len = length(each_seq_sequence)

      # store information in dataframe
      ctg_to_bin_df[each_seq_id, bin_subfolder] = each_bin
      ctg_to_length_df[each_seq_id, 'Ctg_length'] = each_seq_sequence_len
    }
  }
}

# concatenate columns if a contig found in all input  bin subfolders
ctg_to_bin_df$Concate = ifelse(apply(ctg_to_bin_df, 1, function(x) sum(is.na(x))) == 0, col_concat(ctg_to_bin_df, sep = '___'), NA)

# get shared contig sets
shared_ctg_sets = unique(ctg_to_bin_df[["Concate"]])

# remove NA from shared_ctg_sets
shared_ctg_sets_noNA = shared_ctg_sets[!is.na(shared_ctg_sets)]

# initialize shared contig set to total length dataframe
shared_ctg_to_total_length_df = data.frame(matrix(ncol = 2, nrow = 0))
colnames(shared_ctg_to_total_length_df)  = c('Total_length', 'Ctg_list')

# get shared ctg set to total length df
for (shared_ctg_set in shared_ctg_sets_noNA) {
  df_subset = subset(ctg_to_bin_df, ctg_to_bin_df$Concate == shared_ctg_set)
  df_subset_ctgs = row.names(df_subset)
  
  # get total length of each set of shared ctgs
  df_subset_ctgs_total_len = 0
  for(each_ctg in df_subset_ctgs){
    df_subset_ctgs_total_len = df_subset_ctgs_total_len + ctg_to_length_df[each_ctg, 'Ctg_length']
  }
  
  df_subset_ctgs_total_len_Kbp = format(round(df_subset_ctgs_total_len/1024, 2), nsmall = 2)
  df_subset_ctgs_total_len_Kbp_as_double = as.double(df_subset_ctgs_total_len_Kbp)
  shared_ctg_to_total_length_df[shared_ctg_set, 'Total_length'] = df_subset_ctgs_total_len_Kbp_as_double
  shared_ctg_to_total_length_df[shared_ctg_set, 'Ctg_list'] = paste(df_subset_ctgs, collapse = '___')
}

# get refined bin name
refinement_df = shared_ctg_to_total_length_df[order(shared_ctg_to_total_length_df$Total_length, decreasing=TRUE),]
refinement_df$Prefix = output_bin_prefix
refinement_df$ID = seq.int(nrow(refinement_df))
refinement_df$Refined_bin_name = paste(refinement_df$Prefix, refinement_df$ID, sep = "_")

# remove Prefix and IDcolumn from dataframe
refinement_df = within(refinement_df, rm(Prefix, ID))

# remove refined bins with size smaller than provided cutoff
refinement_df = refinement_df[which (refinement_df$Total_length >=minBin_size_Kbp),]

# progress report
if (keep_quiet == FALSE){
  message(paste(Sys.time(), 'Get', length(row.names(refinement_df)), 'refined bins with size larger than', minBin_size_Kbp, 'Kbp'))
  }

#################################### prepare report files ####################################

dir.create(Binning_refiner_wd, showWarnings = FALSE)

# progress report
if (keep_quiet == FALSE){
  message(paste(Sys.time(), 'Prepare report files'))
  }

# prepare df for report
refinement_df_for_report = data.frame(matrix(ncol = 4, nrow = length(row.names(refinement_df))))
colnames(refinement_df_for_report)  = c('Refined_bin', 'Size(Kbp)', 'Source', 'Contigs')
refinement_df_for_report$Refined_bin = refinement_df$Refined_bin_name
refinement_df_for_report$`Size(Kbp)` = refinement_df$Total_length
refinement_df_for_report$Contigs = gsub('___', ',', refinement_df$Ctg_list)
refinement_df_for_report$Source = gsub('___', ',', row.names(refinement_df))

# write out report
write.table(refinement_df_for_report[c(1,2,3)], report_file_sources_and_length, quote = FALSE, sep = "\t", row.names = FALSE)
write.table(refinement_df_for_report[c(1,4)], report_file_contigs, quote = FALSE, sep = "\t", row.names = FALSE)


##################################### prepare sankey plot #####################################

# progress report
if (keep_quiet == FALSE){
  message(paste(Sys.time(), 'Prepare Sankey plot'))
  }

# prepare df for sankey plot
refinement_df_for_plot = data.frame(matrix(ncol = length(input_bin_subfolders) + 2, nrow = length(row.names(refinement_df))))
colnames(refinement_df_for_plot)  = c('Combined', 'Size(Kbp)', input_bin_subfolders)
refinement_df_for_plot$Combined = refinement_df_for_report$Source
refinement_df_for_plot$`Size(Kbp)` = refinement_df_for_report$`Size(Kbp)`
refinement_df_for_plot = separate(refinement_df_for_plot, Combined, input_bin_subfolders, sep = ',', remove = TRUE)

# write out df for sankey plot
close(file(report_file_for_sankey, open = "w"))
write.table('C1,C2,Length_Kbp', report_file_for_sankey, quote = FALSE, sep = ",", row.names = FALSE, col.names = FALSE, append = TRUE)
n = 1
while(n <= length(input_bin_subfolders) -1){
  write.table(refinement_df_for_plot[c(n, n + 1, length(input_bin_subfolders) + 1)], report_file_for_sankey, quote = FALSE, sep = ",", row.names = FALSE, col.names = FALSE, append = TRUE)
  n = n + 1
}

# get sankey plot
my_data = read.csv(report_file_for_sankey, header = TRUE)

if (is.null(sankey_height)){
  sankey_height = length(row.names(refinement_df)) * 12
}

if (is.null(sankey_width)){
  sankey_width = length(input_bin_subfolders)*200
  if (sankey_width < 400){sankey_width = 400}
}

sankey_color_setting = "{node:{colorMode:'unique', labelPadding: 10 },link:{colorMode:'source'}}"

Sankey_plot_my_data <- gvisSankey(my_data, options = list(sankey = sankey_color_setting, height = sankey_height, width = sankey_width))
sink(file = plot_file_for_sankey, append = FALSE, type = c("output", "message"), split = FALSE)
print(Sankey_plot_my_data)
sink()


############################## extract sequence of refined bins ##############################

# progress report
if (keep_quiet == FALSE){
  message(paste(Sys.time(), 'Extract sequences for refined bins'))
  }

# define output bin folder
dir.create(output_bin_folder_name, showWarnings = FALSE)

# extract sequence of refined bins
for (x in row.names(refinement_df)){
  
  refined_bin_name = refinement_df[x, 'Refined_bin_name']
  ctg_id_str = refinement_df[x, 'Ctg_list']
  ctg_id_list = strsplit(ctg_id_str,'___')[[1]]
  ctg_source_bin = strsplit(x,'___')[[1]][1]
  pwd_ctg_source_bin = paste(input_bin_folder, input_bin_subfolders[1], ctg_source_bin, sep = '/')
  pwd_refined_bin = paste(output_bin_folder_name, '/', refined_bin_name, '.fasta', sep = '')

  # initialize fasta file
  close(file(pwd_refined_bin, open = "w"))
  
  # write out needed ctgs
  for (each_seq in read.fasta(file = pwd_ctg_source_bin, seqtype = 'DNA', as.string = TRUE, forceDNAtolower = 0)){
    each_seq_id = getName(each_seq)
    if (any(ctg_id_list == each_seq_id)){
      write.fasta(each_seq, each_seq_id, open = 'a', file.out = pwd_refined_bin)
    }
  }  
}

############################################ Done ############################################

# progress report
if (keep_quiet == FALSE){
  message(paste(Sys.time(), 'Done!'))
}

