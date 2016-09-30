import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages


a = [1,2,3,5,3,4,5,3,4,3,3,4,5]
plt.hist(a)
plt.savefig('hist.png')
plt.close()



utils = rpackages.importr('googleVis')
packages_needed = ['googleVis']
df = robjects.DataFrame.from_csvfile('input_for_googlevis_filtered.csv')
sankey_plot = robjects.r['gvisSankey'](df)

out = open('output.html', 'w')
out.write(str(sankey_plot))
out.close()

