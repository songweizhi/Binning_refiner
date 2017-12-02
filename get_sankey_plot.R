#!/usr/bin/env Rscript
library(tools)
library(optparse)
suppressPackageStartupMessages(library(googleVis))


option_list = list(
  
  make_option(c("-f", "--file"), 
              type="character", 
              default=NULL, 
              help="input file name", 
              metavar="character"),
  
  make_option(c("-x", "--width"), 
              type="double", 
              default=600, 
              help="the width of plot [default= %default]", 
              metavar="double"),
  
  make_option(c("-y", "--height"), 
              type="double", 
              default=1000, 
              help="the height of plot [default= %default]", 
              metavar="double")); 

opt_parser = OptionParser(option_list=option_list);
opt = parse_args(opt_parser);


if (is.null(opt$file)){
  print_help(opt_parser)
  stop("At least one argument must be supplied (input file).n", call.=FALSE)}


my_data = read.csv(opt$file, header = TRUE)
Sankey_plot_my_data <- gvisSankey(my_data, options = list(sankey = "{node:{colorMode:'unique', labelPadding: 10 },link:{colorMode:'source'}}",
                                                       height = opt$height, 
                                                       width = opt$width))

output_file = paste(file_path_sans_ext(opt$file), "html", sep=".")
sink(file = output_file, append = FALSE, type = c("output", "message"), split = FALSE)
print(Sankey_plot_my_data)
sink()
