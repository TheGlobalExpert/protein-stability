"""
data = ProTherm_data()

print(data)
data.info()

data = data[data["ddG"].notna()].reset_index()
data = data.drop(["index", "NO."], axis=1)
print(data)

resolutions = dict()
checked = dict()

high_quality = 0


for i in range(data.shape[0]):
    print(i)

    pdb_id = data.loc[i, "PDB_wild"]

    print(pdb_id)

    try:
        print(resolutions[pdb_id])
        data.loc[i, "resolution"] = resolutions[pdb_id]
        if data.loc[i, "resolution"] <= 2.5:
            high_quality = high_quality + 1
    except:
        try:
            pdb_info =  describe_pdb(data.loc[i, "PDB_wild"])
            print(pdb_info)
            resolution = float(pdb_info["resolution"])


            if resolution <= 2.5:
                resolutions[pdb_id] = resolution
                data.loc[i, "resolution"] = resolution
                high_quality = high_quality + 1
        except:
            data =  data.drop(i)



    checked[pdb_id] = True

print(data.shape)
data.info()
print(len(resolutions))
print(data)
data = data.reset_index()
print(data)
data.to_csv("ProTherm.csv")
"""
#covert units

"""
data = pd.read_csv("ProTherm.csv")


for i in range(data.shape[0]):
    ddG = data.loc[i, "ddG"]
    try:
        data.loc[i, "ddG"] = float(ddG)
    except:

        if ddG[-6:] == "kJ/mol":
            data.loc[i, "ddG"] = round(float(ddG[:-6]) / 4.184,2)
        elif ddG[-8:] == "kcal/mol":
            data.loc[i, "ddG"] = float(ddG[:-8])

    print(data.loc[i, "ddG"])

print(data)
data.to_csv("ProTherm.csv", index=False)

"""
data_pro = pd.read_csv("ProTherm.csv")
"""
data.info()

for i in range(data.shape[0]):

    mut_info = data.loc[i, "MUTATION"].replace(" ", "")

    pdb_id = data.loc[i, "PDB_wild"].lower()

    variant_info =  pdb_id + "_" + mut_info

    data.loc[i, "variant_info"] = variant_info

print(data)
data.to_csv("ProTherm.csv", index=False)
"""
"""
data_hot = pd.read_csv("data/HotMusic_Charlie_doubles_removed.csv")

data_hot.info()

for i in range(data_hot.shape[0]):

    pdb_id = data_hot.loc[i, "PDB"]
    mut_info = data_hot.loc[i, "Variation"]

    variant_info = pdb_id + "_" + mut_info

    data_hot.loc[i, "variant_info"] = variant_info

hot = list(data_hot["variant_info"])
pro = list(data_pro["variant_info"])
n = 0
i = 0
for i in range(data_pro.shape[0]):
    if data_pro.loc[i, "variant_info"] in hot:
        data_pro.drop(i, inplace=True)
        print(i)

print(data_pro)
print(data_hot)

data = pd.concat([data_hot, data_pro])
print(data)
data.to_csv("combined_test.csv")

"""
data = pd.read_csv("combined_test.csv")
print(data)

for i in range(data.shape[0]):
    ddG = data.loc[i, "ddG"]

    if ddG[-1] == ")":
        ddG = ddG[:-3]

    data.loc[i, "ddG"] = float(ddG)

    data.loc[i, "pdb_id"] = data.loc[i, "variant_info"][:4]

    mut_info = data.loc[i, "variant_info"].split("_")[1]

    data.loc[i, "mut_info"] = mut_info
    data.loc[i, "pos"] = mut_info[1:-1]
    data.loc[i, "wt"] = mut_info[0]
    data.loc[i, "mut"] = mut_info[-1]

data.to_csv("ProTherm+HotMusic.csv", index=False)

print(data)
