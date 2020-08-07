import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from tools import Master_results
import math
import matplotlib.style as style

data = pd.read_csv("results/master.csv")
print(data)

labels = "Disulphide breakage,Buried Pro introduced,Clash,Buried hydropilic introduced,Buried charge introduced,Secondary structure altered,Buried charge switch,Disallowed phi/psi,Buried charge replaced,Buried Gly replaced,Buried H-bond breakage,Buried salt bridge breakage,Cavity altered,Buried / exposed switch,Cis pro replaced,Gly in a bend".split(",")

thresholds = [1.0, 1.5, 2.0]

plot_threshold = False
plot_combined = True
plot_abs = True

plt.style.use("seaborn")

output = pd.DataFrame(index=labels, columns=["test", "test"])

def plot_bar_chart(threshold, data):

    for i in range(data.shape[0]):

        ddG = data.loc[i, "ddG"]

        try:
            ddG = ddG.iloc[0]
        except:
            pass
        print(ddG)
        """
        if ddG[-1] == ")":
            ddG = ddG[:-3]
        """
        try:
            ddG = float(ddG)

            if ddG >= threshold:
                data.loc[i, "true_damage"] = 1
            elif ddG < threshold:
                data.loc[i, "true_damage"] = 0
        except:
            data.drop(i)
            exit()

    data.info()
    positive = []
    negative = []

    for i in range(data.shape[0]):
        print(i)
        #print([char for char in data.loc[i, "one_hot_features"]][:-1])
        features = np.array(data.loc[i, labels]).astype(np.float)
        print(features)

        if data.loc[i, "true_damage"] == 1.0:
            positive.append(features)
        elif data.loc[i, "true_damage"] == 0.0:
            negative.append(features)

    positive = np.stack(positive)
    negative = np.stack(negative)
    print(negative)
    print(positive.shape)
    print(negative.shape)

    np.sum(positive, axis=0)

    TPR = np.sum(positive, axis=0)/positive.shape[0]
    FPR = np.sum(negative, axis=0)/negative.shape[0]
    n_positive = positive.shape[0]
    n_negative = negative.shape[0]
    abs_postive = np.sum(positive, axis=0)
    abs_negative = np.sum(negative, axis=0)

    ratios = TPR/FPR


    return ratios, TPR, FPR, n_positive, n_negative, abs_postive, abs_negative


threshold = 1

ratios, TPRs, FPRs, n_positive, n_negative, abs_postive, abs_negative = plot_bar_chart(threshold, data)

CIs_positives = []
CIs_negatives = []

for TPR in TPRs:
    CIs_positives.append(100 * 1.96 * math.sqrt((TPR * (1 - TPR) / n_positive)))

for FPR in FPRs:
    CIs_negatives.append(100 * 1.96 * math.sqrt((FPR * (1 - FPR) / n_negative)))

output["1 - Absolute Postives"] = abs_postive
output["1 - Absolute Negatives"] = abs_negative
output["1 - TPR (%)"] = TPRs *  100
output["1 - FPR (%)"] = FPRs * 100
output["1 - TPR/TPR ratio "] = ratios
output["1 - TPR 95% confidence interval (%)"] = CIs_positives
output["1 - FPR 95% confidence interval (%)"] = CIs_negatives


threshold = 2

ratios, TPRs, FPRs, n_positive, n_negative, abs_postive, abs_negative = plot_bar_chart(threshold, data)

CIs_positives = []
CIs_negatives = []

for TPR in TPRs:
    CIs_positives.append(100 * 1.96 * math.sqrt((TPR * (1 - TPR) / n_positive)))

for FPR in FPRs:
    CIs_negatives.append(100 * 1.96 * math.sqrt((FPR * (1 - FPR) / n_negative)))

output["2 - Absolute Postives"] = abs_postive
output["2 - Absolute Negatives"] = abs_negative
output["2 - TPR (%)"] = TPRs *  100
output["2 - FPR (%)"] = FPRs *  100
output["2 - TPR/TPR ratio "] = ratios
output["2 - TPR 95% confidence interval (%)"] = CIs_positives
output["2 - FPR 95% confidence interval (%)"] = CIs_negatives

print(output)
output.info()
output.to_csv("supplimentary.csv")
