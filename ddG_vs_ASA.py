from tools import HotMusic_data, FoldX, get_ASA
from tqdm import tqdm
import matplotlib.pyplot as plt
import pandas as pd
"""
data = HotMusic_data(data_path="data/HotMusic_Charlie_doubles_removed.csv").dataset

print(data)
print(get_ASA("1bni", 20))

for i in tqdm(range(data.shape[0])):
    try:
        data.loc[i, "ASA"] = get_ASA(data.loc[i, "PDB"], data.loc[i, "location"])
    except:
        pass
    print(data)

data.to_csv("HotMusic_ASA.csv")
"""
data = pd.read_csv("HotMusic_ASA.csv")

ddG = list(data["ddG"])
ASA = list(data["ASA"])

print(len(ddG), len(ASA))

for i in range(len(ASA)):
    ddG[i] = float(ddG[i][:4])
    ASA[i] = float(ASA[i])

print(ddG)
print(ASA)

plt.scatter(ASA, ddG)
plt.xlim(0,10)
plt.show()
