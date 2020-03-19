from tools import Missense3D_data, HotMusic_data
from Bio.Data.IUPACData import protein_letters_3to1
import pandas as pd
import scikitplot as skplt
import matplotlib.pyplot as plt
import decimal
import numpy as np

"""
data = Missense3D_data(tsv_path="analysis.tsv", data_path="Missense3d_results.csv")

missense_data = data.dataset

print(missense_data)

print(missense_data["BoolPrediction"])

hotmusic_data = HotMusic_data().dataset

#Construct labels for comparison

for i in range(missense_data.shape[0]):

    pdb_id = missense_data.loc[i, "#PDB ID"][:4]
    chain = missense_data.loc[i, "#Chain"]
    position = str(missense_data.loc[i, "#PosInPDB"])
    wt = missense_data.loc[i, "#Orig"]
    wt = protein_letters_3to1[wt[0] + wt[1:3].lower()]
    mut = missense_data.loc[i, "#Mutant"]
    mut = protein_letters_3to1[mut[0] + mut[1:3].lower()]


    missense_data.loc[i, "mut_info"] = pdb_id + chain + "_" + wt + position + mut

missense_data.set_index("mut_info", inplace=True)

print(missense_data)

for i in range(hotmusic_data.shape[0]):

    pdb_id = hotmusic_data.loc[i, "PDB"][:4]
    chain = hotmusic_data.loc[i, "chain"]
    mut_info = hotmusic_data.loc[i, "Variation"]

    hotmusic_data.loc[i, "mut_info"] = pdb_id + chain + "_" + mut_info

hotmusic_data.set_index("mut_info", inplace=True)

print(missense_data)
print(hotmusic_data)

missense_data.to_csv("processed_missense.csv")
hotmusic_data.to_csv("processed_hotmusic.csv")
"""

""""
missense_data = pd.read_csv("processed_missense.csv")
hotmusic_data = pd.read_csv("processed_hotmusic.csv")
missense_data.set_index("mut_info", inplace=True)

data = pd.DataFrame()
print(missense_data)

for i in range(hotmusic_data.shape[0]):

    try:
        index = hotmusic_data.loc[i, "mut_info"]
        missense_prediction = int(missense_data.loc[index, "BoolPrediction"])

        ddG = hotmusic_data.loc[i, "ddG"]

        if ddG[-1] == ")":
            ddG = ddG[:-3]

        ddG = float(ddG)
        print(ddG)

        data.loc[index, "missense_prediction"] = missense_prediction
        data.loc[index, "ddG"] = ddG

    except:
        pass

print(data)

data.to_csv("combined.csv")
"""
data_perm = pd.read_csv("data/combined.csv")


def check_accuracy(threshold):
    data = data_perm

    true_positive = 0
    false_positive = 0
    true_negative = 0
    false_negative = 0

    for i in range(data.shape[0]):
        if data.loc[i, "ddG"] >= threshold: #Positve
            if data.loc[i, "missense_prediction"] == 1:
                true_positive = true_positive + 1
            elif data.loc[i, "missense_prediction"] == 0:
                false_positive = false_positive + 1
            else:
                exit()
        else: #negative
            if data.loc[i, "missense_prediction"] == 0:
                true_negative = true_negative + 1
            elif data.loc[i, "missense_prediction"] == 1:
                false_negative = false_negative + 1
            else:
                exit()

    return [true_positive, false_positive, true_negative, false_negative]


results = []

thresholds = list(np.arange(-10,10, 0.1))


print(thresholds)

for threshold in thresholds:
    results.append(check_accuracy(threshold))
    print(threshold)
    pass

print(results)

x = []
y = []

for result in results:
    y.append(result[0] / (result[0] + result[3]))
    x.append(result[1] / (result[1] + result[2]))

x_hori = list(np.arange(0,1.1, 0.1))
y_hori = list(np.arange(0,1.1, 0.1))

print(x_hori)

np.save("missense3d_x_x.npy", x)
np.save("missense3d_y.npy", y)
np.save("roc_thresholds.npy", thresholds)

plt.plot(x,y)
plt.plot(x_hori, y_hori, linestyle="dashed")
plt.xlabel("False Positive Rate")
plt.ylabel("True Postive Rate")
plt.xlim(0,1)
plt.ylim(0,1)
"""
for i in range(len(thresholds)):
    if i % 10 == 0:
        plt.annotate(round(thresholds[i],2), xy=(x[i], y[i]),  xycoords='data',
                xytext=(x[i] - 0.1, y[i]), textcoords='axes fraction',
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='right', verticalalignment='top',
                )
    else:
        pass
"""
plt.title("ROC curve of Missense3D predictions for damaging \n mutations with relation to varying ddG threshold")
plt.show()

"""

data = data_perm

threshold = 2

damage = []
neutral = []

for i in range(data.shape[0]):
    if data.loc[i, "ddG"] > threshold:
        damage.append(data.loc[i, "ddG"])
    else:
        neutral.append(data.loc[i, "ddG"])

print(damage)
print(neutral)

print(len(damage), len(neutral))
"""

"""
for i in range(data.shape[0]):
    if data.loc[i, "ddG"] > threshold:
        data.loc[i, "True"] = 1
    else:
        data.loc[i, "True"] = 0

y_true = np.array(list(data["True"]))
y_probas = np.array(list(data["missense_prediction"]))

y_true = y_true.reshape(len(y_true), 1)
y_true = np.concatenate((1-y_true,y_true),axis=1)

y_probas = y_probas.reshape(len(y_true), 1)
y_probas = np.concatenate((1-y_probas,y_probas),axis=1)

print(y_probas)

skplt.metrics.plot_roc_curve(y_true, y_probas)
plt.show()

print(accuracy)

"""
