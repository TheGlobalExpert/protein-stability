import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

data = pd.read_csv("results/master.csv")

"""
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
"""

def check_accuracy_foldx(threshold):

    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0

    for i in range(data.shape[0]):
        if data.loc[i, "ddG"] >= threshold: #Positve
            if data.loc[i, "foldx_ddG"] >= threshold:
                true_positive = true_positive + 1
            elif data.loc[i, "foldx_ddG"] < threshold:
                false_negative = false_negative + 1
            else:
                exit()
        else: #negative
            if data.loc[i, "foldx_ddG"] < threshold:
                true_negative = true_negative + 1
            elif data.loc[i, "foldx_ddG"] >= threshold:
                false_positive = false_positive + 1
            else:
                exit()

    return [true_positive, false_positive, true_negative, false_negative]

def check_accuracy_missense(threshold):

    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0

    for i in range(data.shape[0]):
        if data.loc[i, "ddG"] >= threshold: #Positve
            if int(data.loc[i, "missense_damaging"]) == 1:
                true_positive = true_positive + 1
            else:
                false_negative = false_negative + 1

        else: #negative
            if int(data.loc[i, "missense_damaging"]) == 0:
                true_negative = true_negative + 1
            else:
                false_positive = false_positive + 1



    return [true_positive, false_positive, true_negative, false_negative]

def TPR(true_positive, false_positive, true_negative, false_negative):

    return true_positive / (true_positive + false_negative)

def FPR(true_positive, false_positive, true_negative, false_negative):

    return false_positive / (false_positive + true_negative)

thresholds = list(np.arange(-20, 30, 0.5))

foldx_TPR = []
foldx_FPR = []

for threshold in thresholds:

    print(threshold)

    true_positive, false_positive, true_negative, false_negative = check_accuracy_foldx(threshold)

    try:
        foldx_TPR.append(TPR(true_positive, false_positive, true_negative, false_negative))
    except:
        foldx_TPR.append(np.nan)

    try:
        foldx_FPR.append(FPR(true_positive, false_positive, true_negative, false_negative))
    except:
        foldx_FPR.append(np.nan)

missense_TPR = []
missense_FPR = []

thresholds = [1.0, 1.5, 2.0]

for threshold in thresholds:

    print(threshold)

    true_positive, false_positive, true_negative, false_negative = check_accuracy_missense(threshold)

    try:
        missense_TPR.append(TPR(true_positive, false_positive, true_negative, false_negative))
    except:
        missense_TPR.append(np.nan)

    try:
        missense_FPR.append(FPR(true_positive, false_positive, true_negative, false_negative))
    except:
        missense_FPR.append(np.nan)

print(foldx_TPR, foldx_FPR)

#---Parameters---

foldx_toi = [100,103, 105, 107, 110, 112,116, 118, 120]
missense3d_toi = [100,103, 105, 107, 110, 112,114,116, 118, 120]

#---Figure---

plt.figure(figsize = (6,6))
plt.plot(foldx_FPR,foldx_TPR, label="FoldX")
plt.scatter(missense_FPR,missense_TPR, color=  "orange", label="Missense3D")
#plt.plot(x_hori, y_hori, linestyle="dashed")
plt.xlabel("False Positive Rate")
plt.ylabel("True Postive Rate")
plt.xlim(0,1)
plt.ylim(0,1)
#plt.title("ROC curve of FoldX and Missense3D predictions of thermal\nstability with relation to varying ddG threshold (HotMusic dataset)")
plt.legend()

x_hori = list(np.arange(0,1.1, 0.1))
y_hori = list(np.arange(0,1.1, 0.1))
plt.plot(x_hori, y_hori, linestyle="dashed")
"""
for threshold in foldx_toi:
    plt.text(foldx_x[threshold] - 0.06, foldx_y[threshold] + 0.01, str(abs(round(thresholds[threshold],3))))
    plt.scatter(foldx_x[threshold], foldx_y[threshold], c="teal")

for threshold in missense3d_toi:
    plt.text(missense3d_x[threshold] - 0.06, missense3d_y[threshold] + 0.01, str(abs(round(thresholds[threshold],3))))
    plt.scatter(missense3d_x[threshold], missense3d_y[threshold], c="orange")

#Calc AUROC

AUROC = 0

for i in range(1, len(foldx_x)):
    base = (foldx_x[i-1] - foldx_x[i]) * foldx_y[i]
    top = ((foldx_x[i-1] - foldx_x[i]) * (foldx_y[i-1] - foldx_y[i])) / 2
    total = base + top
    print(total)
    if math.isnan(total):
        pass
    else:
        AUROC = AUROC + total

print("FoldX", AUROC)

AUROC = 0

for i in range(1, len(foldx_x)):
    base = (missense3d_x[i-1] - missense3d_x[i]) * missense3d_y[i]
    top = ((missense3d_x[i-1] - missense3d_x[i]) * (missense3d_y[i-1] - missense3d_y[i])) / 2
    total = base + top
    if math.isnan(total):
        pass
    else:
        AUROC = AUROC + total

print("Missense3D", AUROC)
"""
plt.show()
