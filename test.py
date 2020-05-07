from tools import *
import pandas as pd

data = Master_results()
data.info()

for i in range(data.shape[0]):

    if data.loc[i, "wt"] == "C":
        print(data.loc[i, "ddG"], data.loc[i, "variant_info"])