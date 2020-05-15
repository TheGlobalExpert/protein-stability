from tools import HotMusic_data, FoldX
import pandas as pd
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt

print("# WARNING: running this program will delete previous data")

#data = pd.read_csv("data/ProTherm+HotMusic.csv")
data = pd.read_csv("data/FoldX_predictions.csv")
data.info()

for i in range(data.shape[0]):

    if data.loc[i, "ddG"][-1] == ")":

        data.loc[i, "ddG"] = float(data.loc[i, "ddG"][:-3])

    data.loc[i, "ddG"] = float(data.loc[i, "ddG"])
    data.loc[i, "FoldX_dGG"] = float(data.loc[i, "FoldX_dGG"])

    pH = data.loc[i, "pH "]

    if data.loc[i, "Temp"] != "25":
        print("AHH")
        data.drop(i, axis=0, inplace=True)
    """

    elif data.loc[i, "pH "] != "7":
        print("AHH")
        data.drop(i, axis=0, inplace=True)
    """



data.dropna(subset=["ddG", "FoldX_dGG"] ,inplace=True)



data.reset_index()
print(data.shape)

data.info()

x = np.array(data["ddG"], dtype=float)
y = np.array(data["FoldX_dGG"], dtype=float)
print(x.shape)

"""
for i in range(len(x)):
    print(x[i])
    print(y[i])
    """


plt.scatter(x, y)


plt.ylabel("Predicted ddG")
plt.xlabel("Experimental ddG")
x_temp = np.array(x)

corr = np.corrcoef(x, y)[0,1]
plt.text(-2.5, 5, 'Spearman correlation \ncoefficent: '+str(round(corr,3)))
print(corr)


m, b = np.polyfit(x, y, 1)
plt.plot(x_temp, m*x_temp + b, label="Best Fit")
plt.text(3.3, -1.3, 'slope = '+str(round(m,2)))
plt.text(3.3, -1.7, 'y-intercept = '+str(round(b,2)))

plt.ylim(-3,6)
plt.xlim(-3,6)
plt.title("Variants only at 25C (n=556)")

plt.show()
