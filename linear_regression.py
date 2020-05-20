from tools import HotMusic_data, FoldX
import pandas as pd
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

#---Load and prepare data----#

data = pd.read_csv("results/master.csv")

x = np.array(data["ddG"], dtype=float)
y = np.array(data["foldx_ddG"], dtype=float)

#----Render plot----#

plt.scatter(x, y, s=4)
plt.ylabel("Predicted ddG (kcal/mol)")
plt.xlabel("Experimental ddG (kcal/mol)")

#Correlation coefficent
corr = np.corrcoef(x, y)[0,1]
print("Correlation coefficent = ", corr)
#plt.text(-2.5, 5, 'Pearson correlation \ncoefficent: '+str(round(corr,3)))


#Linear regression analysis
x_temp = np.array(x)
m, c = np.polyfit(x, y, 1)
print("m = ", m)
print("c = ", c)

plt.plot(x_temp, m*x_temp + c, "red", label="Best Fit")
"""
plt.text(3.3, -1.3, 'slope = '+str(round(m,2)))
plt.text(3.3, -1.7, 'y-intercept = '+str(round(c,2)))
"""

#Plot ideal
plt.plot(range(-10,10), range(-10,10), "orange", linestyle="--", label="Ideal")


#----Formatting----#
plt.gca().spines['right'].set_position('zero')
plt.gca().spines['top'].set_position('zero')

plt.gca().xaxis.set_ticks_position('bottom')
plt.gca().yaxis.set_ticks_position('left')

plt.axis("equal")
plt.ylim(-7,30)
plt.xlim(-10,10)
#plt.ylim(-3,6)
#plt.xlim(-3,6)
plt.legend()
plt.tight_layout()
plt.show()
