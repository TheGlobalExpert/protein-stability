from tools import Master_results
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = Master_results()

def concordance_matrix(threshold):

    M_Y_F_Y = 0
    M_Y_F_N = 0
    M_N_F_Y = 0
    M_N_F_N = 0

    for i in range(data.shape[0]):

        if data.loc[i, "FoldX_ddG"] >= threshold:
            if data.loc[i, "BoolPrediction"] == 1:
                M_Y_F_Y = M_Y_F_Y + 1
            elif data.loc[i, "BoolPrediction"] == 0:
                M_N_F_Y = M_N_F_Y + 1

        elif data.loc[i, "FoldX_ddG"] < threshold:
            if data.loc[i, "BoolPrediction"] == 1:
                M_Y_F_N = M_Y_F_N + 1
            elif data.loc[i, "BoolPrediction"] == 0:
                M_N_F_N = M_N_F_N + 1

    return [M_Y_F_Y, M_Y_F_N, M_N_F_Y, M_N_F_N]

thresholds = [1.0, 1.5, 2.0]

for threshold in thresholds:

    print(threshold, concordance_matrix(threshold))


print(concordance_matrix(1.5))

thresholds = np.arange(0, 5.1, 0.1)

values = []

for threshold in thresholds:

    values.append(np.array(concordance_matrix(threshold)))
    print(threshold)

total = np.sum(values[0])

values = np.stack(values)*100/total


for i in range(4):
    plt.plot(values[:,i])
plt.legend(["Missense_Y_FoldX_Y", "Missense_Y_FoldX_N", "Missense_N_FoldX_Y", "Missense_N_FoldX_N"])
plt.xticks(range(0,51,10), [0,1,2,3,4,5])
plt.ylabel("%")
plt.xlabel("ddG Threshold")
plt.show()
