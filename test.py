import pandas as pd

data = pd.read_csv("FoldX_predictions.csv")

pdb_ids = list(data["PDB"])

dict = {}

for pdb_id in pdb_ids:
    dict[pdb_id] = 1

print(len(dict))
