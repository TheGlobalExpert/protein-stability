from tools import *
import pandas as pd
from pypdb import describe_pdb

"""
data = pd.read_csv("data/processed_hotmusic.csv")

data.info()

for i in range(data.shape[0]):

    if len(data.loc[i, "PDB"]) > 4:
        print("AHHH")

        data.drop(i, inplace=True)

    elif data.loc[i, "ddG"] == "-":
        print("what?")
        data.drop(i, inplace=True)

    else:

        try:
            float(data.loc[i, "ddG"])
        except:
            print(data.loc[i, "ddG"][:-3])
            data.loc[i, "ddG"] = float(data.loc[i, "ddG"][:-3])

data.reset_index(inplace=True)

data.info()

data.to_csv("test.csv")
"""

data = pd.read_csv("test.csv")

for i in range(data.shape[0]):

    float(data.loc[i, "ddG"])
    float(data.loc[i, "Temp"])
    float(data.loc[i, "pH"])
    print(i)

data.info()

for i in range(data.shape[0]):

    data.loc[i, "foldx_ddG"] = FoldX(data.loc[i, "PDB"], mode=position_scan, mutation=mut_info, temp=data.loc[i, "Temp"], pH=data.loc[i, "pH"]).ddG

    data.to_csv("foldx2.csv")
