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

data = {"x":x,"y":y}
plt.scatter("x","y", data=data, label=None)

plt.plot(x,y,"o")

plt.ylabel("Predicted ddG")
plt.xlabel("Experimental ddG")
x = np.array(x)
#plt.xticks(np.arange(x.min(), x.max(), 0.5))
corr = np.corrcoef(x, y)[0,1]
plt.text(-2.5, 7, 'Spearman correlation \ncoefficent: '+str(round(corr,3)))
print(corr)

m, b = np.polyfit(x, y, 1)
plt.plot(x, m*x + b, label="Best Fit")
plt.text(3.3, -1.3, 'slope = '+str(round(m,2)))
plt.text(3.3, -1.7, 'y-intercept = '+str(round(b,2)))

x_hori = list(np.arange(-10,10, 0.5))
y_hori = list(np.arange(-10,10, 0.5))


plt.plot(x_hori, y_hori, linestyle="dashed", label="Ideal")
plt.ylim(-3,8)
plt.xlim(-3,6)
plt.legend(loc="upper right")
plt.title("Scatter plot of FoldX predicted ddG verus \nexperimentally determined ddG (HotMusic dataset)")

plt.show()



print(x)
print(y)

def check_accuracy(threshold):

    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0

    for i in range(data.shape[0]):
        if data.loc[i, "ddG"] >= threshold: #Positve
            if data.loc[i, "FoldX_predictions"] >= threshold:
                true_positive = true_positive + 1
            elif data.loc[i, "FoldX_predictions"] <= threshold:
                false_positive = false_positive + 1
            else:
                exit()
        else: #negative
            if data.loc[i, "FoldX_predictions"] <= threshold:
                true_negative = true_negative + 1
            elif data.loc[i, "FoldX_predictions"] >= threshold:
                false_negative = false_negative + 1
            else:
                exit()

    return [true_positive, false_positive, true_negative, false_negative]

def check_accuracy(threshold, x, y):

    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0

    for i in range(len(x)):
        if float(x[i]) >= threshold: #Positve
            if y[i] >= threshold:
                true_positive = true_positive + 1
            elif y[i] <= threshold:
                false_positive = false_positive + 1
            else:
                exit()
        else: #negative
            if y[i] <= threshold:
                true_negative = true_negative + 1
            elif y[i] >= threshold:
                false_negative = false_negative + 1
            else:
                exit()

    return [true_positive, false_positive, true_negative, false_negative]


results = []

thresholds = list(np.arange(-10,10, 0.1))


print(thresholds)

for threshold in thresholds:
    results.append(check_accuracy(threshold, x, y))
    print(threshold)
    pass

print(results)

x = []
y = []

for i, result in enumerate(results):
    print(result)
    try:
        x.append(result[1] / (result[1] + result[2]))
        y.append(result[0] / (result[0] + result[3]))
    except:
        x.append(np.nan)
        y.append(np.nan)

print(x)


for i in range(len(x)):
    print(i, "----")
    print(x[i])
    print(results[i])

x_hori = list(np.arange(0,1.1, 0.1))
y_hori = list(np.arange(0,1.1, 0.1))

TOI = [100,103, 105, 107, 110, 112, 118, 120]
plt.figure(figsize = (6,6))
for threshold in TOI:
    plt.text(x[threshold] - 0.06, y[threshold] + 0.01, str(round(thresholds[threshold],3)))
    #print(thresholds[threshold], threshold)



plt.plot(x,y)
plt.plot(x_hori, y_hori, linestyle="dashed")
plt.xlabel("False Positive Rate")
plt.ylabel("True Postive Rate")
plt.xlim(0,1)
plt.ylim(0,1)
plt.title("ROC curve of FoldX predictions of ddG with relation\nto varying ddG threshold (HotMusic dataset)")

for threshold in TOI:
    plt.scatter(x[threshold], y[threshold], c="b")

plt.show()
