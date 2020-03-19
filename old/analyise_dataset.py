import pandas as pd
import numpy as np

dataset = pd.read_csv("HotMusic_dataset.csv")

print(dataset)

for i in range(dataset.shape[0]):
	if dataset.loc[i, "ddG"] == "-":
		dataset.drop(i, inplace=True)
	elif len(dataset.loc[i, "PDB"]) > 4:
		dataset.drop(i, inplace=True)

dataset.reset_index(inplace=True)

print(dataset)

dataset.to_csv("HotMusic_Charlie.csv")

#raw = 1626
#without ddG = 1147
#and with doubles = 1102
