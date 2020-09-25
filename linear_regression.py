#################################################################
#                                                               #
#    Linear regression analysis between our FoldX predicted     #
#           and experimentally determined folding ddGs          #
#                                                               #
#################################################################

from tools import HotMusic_data, FoldX
import pandas as pd
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#---Load and prepare data----#

data = pd.read_csv("results/master.csv")

x = np.array(data["ddG"], dtype=float)
y = np.array(data["foldx_ddG"], dtype=float)

#----Render plot----#

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8,4))

ax1.scatter(x, y, s=4)
ax1.set_ylabel("Predicted \u0394\u0394G (kcal/mol)")
ax1.set_xlabel("Experimental \u0394\u0394G (kcal/mol)")

#Correlation coefficent
corr = np.corrcoef(x, y)[0,1]
print("Correlation coefficent = ", corr)
#plt.text(-2.5, 5, 'Pearson correlation \ncoefficent: '+str(round(corr,3)))


#Linear regression analysis
x_temp = np.array(x)
m, c = np.polyfit(x, y, 1)
print("m = ", m)
print("c = ", c)

ax1.plot(x_temp, m*x_temp + c, "red", label="Best Fit")
"""
plt.text(3.3, -1.3, 'slope = '+str(round(m,2)))
plt.text(3.3, -1.7, 'y-intercept = '+str(round(c,2)))
"""

#Plot ideal
ax1.plot(range(-10,10), range(-10,10), "orange", linestyle="--", label="Ideal")

ax2 = sns.boxplot(data=data[["ddG", "foldx_ddG"]])
ax2.set(xlabel="Data source", ylabel="\u0394\u0394G (kcal/mol)", xticklabels=["Experimental", "Predicted (FoldX)"])

#----Formatting----#
ax1.spines['right'].set_position('zero')
ax1.spines['top'].set_position('zero')

ax1.xaxis.set_ticks_position('bottom')
ax1.yaxis.set_ticks_position('left')

ax1.axis("equal")

ax1.set_title("A", loc="left", fontweight="bold")
ax2.set_title("B", loc="left", fontweight="bold")

#plt.ylim(-7,30)
#plt.xlim(-10,10)
ax1.set_ylim(-3,6)
ax1.set_xlim(-3,6)
ax1.legend()
plt.tight_layout()
plt.savefig("figs/linear_regression.png", dpi=400)
plt.show()
