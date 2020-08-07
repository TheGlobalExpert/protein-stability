import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from tools import Master_results
import math
import matplotlib.style as style
import seaborn as sns
import statistics

data = pd.read_csv("results/master.csv")
print(data)

labels = "Disulphide breakage,Buried Pro introduced,Clash,Buried hydropilic introduced,Buried charge introduced,Secondary structure altered,Buried charge switch,Disallowed phi/psi,Buried charge replaced,Buried Gly replaced,Buried H-bond breakage,Buried salt bridge breakage,Cavity altered,Buried / exposed switch,Cis pro replaced,Gly in a bend".split(",")

thresholds = [1.0, 2.0]

plot_threshold = False
plot_combined = True
plot_abs = True

plt.style.use("seaborn")

label_errors = []

errors = pd.DataFrame([], columns=["error", "label"])
print(errors)
for label in labels:


    for i in range(data.shape[0]):
        print(i)
        if data.loc[i, label] == 1.0:
            to_add = pd.Series([data.loc[i, "foldx_ddG"] - data.loc[i, "ddG"], label], index = errors.columns)
            errors = errors.append(to_add, ignore_index=True)
        else:
            pass

for label in labels:

    temp = errors[(errors["label"] == label)]

    print(label, "\n",statistics.median(list(temp["error"])))

print(errors)

ax = sns.boxplot(x="label", y="error", data=errors, color="C0")
ax.set_xticklabels(labels, rotation=55,  horizontalalignment='right')
ax.set_xlabel("")
ax.set_ylabel("FoldX \u0394\u0394G prediction error (kcal/mol)")
plt.tight_layout()
plt.savefig("error.png", dpi=400)
plt.show()
