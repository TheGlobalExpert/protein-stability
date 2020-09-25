#################################################################
#                                                               #
# Python script to calculate the errors between FoldX predicted #
#    ddGs and experimental for particular structural features   #
#                                                               #
#################################################################

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from tools import Master_results
import math
import matplotlib.style as style
import seaborn as sns
import statistics

#----Load data----#

data = pd.read_csv("results/master.csv")

#----Initisialise----#

labels = "Disulphide breakage,Buried Pro introduced,Clash,Buried hydropilic introduced,Buried charge introduced,Secondary structure altered,Buried charge switch,Disallowed phi/psi,Buried charge replaced,Buried Gly replaced,Buried H-bond breakage,Buried salt bridge breakage,Cavity altered,Buried / exposed switch,Cis pro replaced,Gly in a bend".split(",")
plt.style.use("seaborn")
label_errors = []
errors = pd.DataFrame([], columns=["error", "label"])

#----Calculate errors between FoldX and experimental values for each structural feature----#


for label in labels:    # Iterate by feature

    for i in range(data.shape[0]):    # Iterate by every variant

        if data.loc[i, label] == 1.0:   # Check if structural feature is observed in that variant

            # Calculate ddG error
            to_add = pd.Series([data.loc[i, "foldx_ddG"] - data.loc[i, "ddG"], label], index = errors.columns)
            # Add to errors dataframe
            errors = errors.append(to_add, ignore_index=True)

        else:
            pass


#----Plot Figure----#

ax = sns.boxplot(x="label", y="error", data=errors, color="C0")
ax.set_xticklabels(labels, rotation=55,  horizontalalignment='right')
ax.set_xlabel("")
ax.set_ylabel("FoldX \u0394\u0394G prediction error (kcal/mol)")
plt.tight_layout()
plt.savefig("error.png", dpi=400)
plt.show()
