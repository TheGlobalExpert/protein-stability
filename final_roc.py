import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

#---Data---

foldx_x = np.load("results/foldx_x.npy")
foldx_y = np.load("results/foldx_y.npy")

missense3d_x = np.load("results/missense3d_x.npy")
missense3d_y = np.load("results/missense3d_y.npy")

thresholds = np.load("results/roc_thresholds.npy")

x_hori = list(np.arange(0,1.1, 0.1))
y_hori = list(np.arange(0,1.1, 0.1))

#Clean data

for i in range(len(foldx_x)):
    if i < 81:
        foldx_x[i] = np.nan

#---Parameters---

foldx_toi = [100,103, 105, 107, 110, 112,116, 118, 120]
missense3d_toi = [100,103, 105, 107, 110, 112,114,116, 118, 120]

#---Figure---

plt.figure(figsize = (6,6))
plt.plot(foldx_x,foldx_y, label="FoldX")
plt.plot(missense3d_x,missense3d_y, label="Missense3D")
plt.plot(x_hori, y_hori, linestyle="dashed")
plt.xlabel("False Positive Rate")
plt.ylabel("True Postive Rate")
plt.xlim(0,1)
plt.ylim(0,1)
#plt.title("ROC curve of FoldX and Missense3D predictions of thermal\nstability with relation to varying ddG threshold (HotMusic dataset)")
plt.legend()

for threshold in foldx_toi:
    plt.text(foldx_x[threshold] - 0.06, foldx_y[threshold] + 0.01, str(abs(round(thresholds[threshold],3))))
    plt.scatter(foldx_x[threshold], foldx_y[threshold], c="teal")

for threshold in missense3d_toi:
    plt.text(missense3d_x[threshold] - 0.06, missense3d_y[threshold] + 0.01, str(abs(round(thresholds[threshold],3))))
    plt.scatter(missense3d_x[threshold], missense3d_y[threshold], c="orange")

plt.show()
