### plotting heatmap from data
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

###  Read data from txt ###
max_iter = 25
f = 4
N = 35
sigma = 0
#infile = open("./validation-map-iterations-{:d}-f{:d}-filter05.txt".format(max_iter,f), "r")
infile = open("./validation-map-iterations-{:d}-f{:d}-N{:d}-filter00.txt".format(max_iter,f,N), "r")
accuracy = np.loadtxt(infile)
infile.close()

### Make heatmeap
# Set up the dataframe
dw = 0.05
end = 1.0
start = 0.2
n_points = int((end-start)/dw)
w = np.linspace(start,end, n_points+1)

colvec = np.linspace(0,max_iter,max_iter)
colvec = ["%d" % x for x in colvec]
row_vec = ["%.2f" % x for x in w]

ac = pd.DataFrame(accuracy, columns = [colvec], index = [row_vec])
# Use dataframe and make a heatmap
#plt.title("T:{:.2f}, MC: {:d}".format(float(T),Ncycles), fontsize = 14)
fs1 = 14
fs = 20
plt.figure(figsize = (10,6))
cmap = sns.diverging_palette(220, 20, sep=20, as_cmap=True)
ax = sns.heatmap(ac, vmin = 0.001, vmax = 0.4,cbar_kws={'label': 'Accuracy'})#, cmap = cmap)#,cmap="RdYlGn")
plt.xlabel("Iterations", fontsize = fs)
plt.ylabel("Smoothing parameter", fontsize = fs)
plt.xticks(fontsize = fs1)
plt.yticks(fontsize = fs)
cbar = ax.collections[0].colorbar
cbar.ax.tick_params(labelsize=fs)
ax.figure.axes[-1].yaxis.label.set_size(fs)
plt.tight_layout()
plt.savefig("heatmap-N{:d}-filter-0{:d}.pdf".format(N,sigma),format = "pdf")
plt.show()
