import pandas as pd
import urllib.request
import os

data = pd.read_csv("../data/ProTherm+HotMusic.csv")
pdb_ids = list(data["pdb_id"])

#Clean PDB tags
for i in range(len(pdb_ids)):
    pdb_ids[i] = pdb_ids[i][:4]

#Remove duplicates
pdb_ids = list(dict.fromkeys(pdb_ids))
print(pdb_ids)
print(len(pdb_ids))

#Fetch files
for pdb_id in pdb_ids:
    print(pdb_id)
    fullfilename = "../files/pdb/" + pdb_id + ".pdb"
    if os.path.isfile(fullfilename): # File in directory
        pass
    else:
        urllib.request.urlretrieve('http://files.rcsb.org/download/' +
                                        pdb_id.upper() + '.pdb',
                                        fullfilename)
