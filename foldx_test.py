from tools import HotMusic_data, FoldX
import pandas as pd
from tqdm import tqdm
import numpy as np

print("# WARNING: running this program will delete previous data")

#data = pd.read_csv("data/ProTherm+HotMusic.csv")
data = pd.read_csv("FoldX_predictions.csv")
data.info()
"""
for i in tqdm(range(data.shape[0])):
    print(data.loc[i, "FoldX_dGG"])
    print(i)
    print(data.loc[i, "pdb_id"])
    print(data.loc[i, "mut_info"])

    if pd.isna(data.loc[i, "FoldX_dGG"]) == True:
        mutation = data.loc[i, "wt"] + "A" + str(data.loc[i, "pos"]) + data.loc[i, "mut"]
        print(mutation)
        data.loc[i, "FoldX_dGG"] = FoldX(data.loc[i, "pdb_id"], mode="position_scan", mutation=mutation).ddG

    #data.to_csv("FoldX_predictions.csv", index=False)
print(data)
"""
