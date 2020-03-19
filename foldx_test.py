from tools import HotMusic_data, FoldX
from tqdm import tqdm

print("# WARNING: running this program will delete previous data")

"""
data = HotMusic_data(data_path="data/HotMusic_Charlie_doubles_removed.csv").dataset

print(data)


for i in tqdm(range(data.shape[0])):

    mutation = data.loc[i, "wt"] + data.loc[i, "chain"] + data.loc[i, "location"] + data.loc[i, "mut"]

    try:
        data.loc[i, "FoldX_dGG"] = FoldX(data.loc[i, "PDB"], mode="position_scan", mutation=mutation).ddG
    except:
        pass

    data.to_csv("FoldX_predictions.csv", index=False)
"""
