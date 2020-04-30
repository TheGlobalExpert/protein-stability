import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

data = pd.read_csv("FoldX_predictions.csv")

x = list(data["ddG"])
y = list(data["FoldX_dGG"])

#clean # XXX:

for i in range(len(x)):
    if x[i][-1] == ")":
        x[i] = x[i][:-3]

indexes = []
for i in range(len(x)):
    print(len(y))
    if math.isnan(y[i]) == True:
        indexes.append(i)

for i in reversed(indexes):
    del x[i]
    del y[i]


import itertools

#lists = sorted(zip(*[x, y]))
#x, y = list(zip(*lists))
#x = x[:10]
#y = y[:10]

for i in range(len(x)):
    x[i] = float(x[i])

print(y)
print(x)
x = np.array(x)
y = np.array(y)



print(x)
print(y)



def check_absolutes(real_threshold, foldx_threshold, x, y):

    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0

    for i in range(len(x)):
        if float(x[i]) >= foldx_threshold: #Positve
            if y[i] >= real_threshold:
                true_positive = true_positive + 1
            elif y[i] <= real_threshold:
                false_positive = false_positive + 1
            else:
                exit()
        else: #negative
            if y[i] <= real_threshold:
                true_negative = true_negative + 1
            elif y[i] >= real_threshold:
                false_negative = false_negative + 1
            else:
                exit()

    return true_positive, false_positive, true_negative, false_negative

def ROC_values(real_threshold, x, y):
    thresholds = list(np.arange(-10,10, 0.1))

    TPR = []
    FPR = []



    for foldx_threshold in thresholds:

        true_positive, false_positive, true_negative, false_negative = check_absolutes(real_threshold, foldx_threshold, x, y)

        try:
            TPR.append(true_positive / (true_positive+false_negative))
        except:
            TPR.append(np.nan)


        try:
            FPR.append(false_positive / (false_positive+true_negative))
        except:
            FPR.append(np.nan)

    return TPR, FPR


#---Data---

missense3d_x = np.load("results/missense3d_x.npy")
missense3d_y = np.load("results/missense3d_y.npy")

thresholds = np.load("results/roc_thresholds.npy")

x_hori = list(np.arange(0,1.1, 0.1))
y_hori = list(np.arange(0,1.1, 0.1))

#---Parameters---

real_thresholds = [1.0, 1.5 , 2.0]
colours = ["blue", "orange", "green"]

foldx_toi = [110, 115, 120]
missense3d_toi = [110, 115, 120]

#---Figure---

plt.figure(figsize = (7,7))

for real_threshold, colour in zip(real_thresholds, colours):
    TPR, FPR = ROC_values(real_threshold, x, y)
    print(TPR)
    print(FPR)

    plt.plot(FPR, TPR, label=real_threshold, color=colour)

    foldx_thresholds = list(np.arange(-10,10, 0.1))

    shapes = ["o", "^", "s"]

    for threshold, shape in zip(foldx_toi, shapes):

        if real_threshold == 1.5:
            plt.text(FPR[threshold] - 0.05, TPR[threshold] + 0.01, str(abs(round(foldx_thresholds[threshold],3))))
        plt.scatter(FPR[threshold], TPR[threshold], c=colour, marker=shape)

shapes = ["o", "^", "s"]
plot_thresholds = ["= 1.0", "= 1.5", "= 2.0"]

plt.text(0.7, 0.24, "FoldX threshold:")

for i, shape in enumerate(shapes):

    plt.scatter(0.8, 0.2 - i*0.05, marker=shape, color="black")
    plt.text(0.82, 0.19 - i*0.05, plot_thresholds[i])


plt.plot(x_hori, y_hori, linestyle="dashed")
plt.xlabel("False Positive Rate")
plt.ylabel("True Postive Rate")
plt.xlim(0,1)
plt.ylim(0,1)
#plt.title("ROC curve of FoldX and Missense3D predictions of thermal\nstability with relation to varying ddG threshold (HotMusic dataset)")


"""
for threshold in foldx_toi:
    plt.text(foldx_x[threshold] - 0.06, foldx_y[threshold] + 0.01, str(abs(round(thresholds[threshold],3))))
    plt.scatter(foldx_x[threshold], foldx_y[threshold], c="teal")
"""

for threshold, shape in zip(missense3d_toi, shapes):
    plt.text(missense3d_x[threshold] + 0.02, missense3d_y[threshold] + 0.01, str(abs(round(thresholds[threshold],3))))
    if threshold == 110:
        plt.scatter(missense3d_x[threshold], missense3d_y[threshold], c="red", marker="*", label="Missense3D")
    else:
        plt.scatter(missense3d_x[threshold], missense3d_y[threshold], c="red", marker="*")
plt.legend(title="Real threshold")
plt.show()
