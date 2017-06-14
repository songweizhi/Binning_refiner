import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages

def GoogleVis_Sankey_plotter(input_csv, output_html, height):
    out = open(output_html, 'w')
    utils = rpackages.importr('googleVis')
    packages_needed = ['googleVis']
    for each_package in packages_needed :
        if not rpackages.isinstalled(each_package):
            utils.install_packages(each_package)
        else:
            pass

    df = robjects.DataFrame.from_csvfile(input_csv)
    sankey_plot = robjects.r['gvisSankey'](df,
                                           option = robjects.r['list'](
                                               sankey = "{node : {colorMode: 'unique', labelPadding: 10}, link:{colorMode: 'source'}}",
                                               height = height,
                                               width = 600))
    out.write(str(sankey_plot))
    out.close()
