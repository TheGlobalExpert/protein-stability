from tools import HotMusic_data, FoldX
from tqdm import tqdm

print("# WARNING: running this program will delete previous data")

data = pd.read_csv("data\ProTherm+HotMusic.csv")


for i in tqdm(range(data.shape[0])):

    mutation = data.loc[i, "wt"] + "A" + data.loc[i, "loc"] + data.loc[i, "mut"]

    try:
        data.loc[i, "FoldX_dGG"] = FoldX(data.loc[i, "pdb"], mode="position_scan", mutation=mutation).ddG
    except:
        pass

    data.to_csv("FoldX_predictions.csv", index=False)
