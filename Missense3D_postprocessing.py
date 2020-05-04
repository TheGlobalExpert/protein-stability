from tools import Missense3D_data, HotMusic_data, Master_results
from Bio.Data.IUPACData import protein_letters_3to1
import pandas as pd
import scikitplot as skplt
import matplotlib.pyplot as plt
import decimal
import numpy as np
"""
data = Missense3D_data(tsv_path="results/missense3d/analysis.tsv").dataset
#=data.to_csv("temp.csv", index=False)

#data = pd.read_csv("temp.csv")
print(data)
data.info()

drop = list(data.columns[:-3])

print(drop)

data.drop(drop, axis=1, inplace=True)

data.info()
print(data)

data1 = data
data2 = Master_results()
data1.info()
data2.info()


data1.set_index("variant_info", inplace=True, drop=True)
data2.set_index("variant_info", inplace=True, drop=True)

data1 = data1.loc[~data1.index.duplicated(keep='first')]
data2 = data2.loc[~data2.index.duplicated(keep='first')]

data1.info()
data2.info()

x = 0
for i in data2.index:
    print(i)
    print(x)
    x=x+1

    data2.loc[i, "one_hot_features"] = data1.loc[i, "one_hot_features"] + "x"
    data2.loc[i, "BoolPrediction"] = data1.loc[i, "BoolPrediction"]


print(data2)
data2.info()

data2.to_csv("master.csv")
"""

data = Master_results()
print(data)