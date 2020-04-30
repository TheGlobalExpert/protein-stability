import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pypdb import describe_pdb
import os, sys
import tqdm

def ProTherm_data():

    data_path = "data/ProTherm+HotMusic.csv"

    dataset = pd.read_csv(data_path)

    return dataset

class HotMusic_data(object):

    def __init__(self, data_path="HotMusic_dataset.csv"):
        self.data_path = data_path

        self.load_dataset()

    def load_dataset(self):

        dataset = pd.read_csv(self.data_path)

        variations = list(dataset["Variation"])

        for i, variation in enumerate(variations):
        	dataset.loc[i,"wt"] = variation[0]
        	dataset.loc[i,"mut"] = variation[-1]
        	dataset.loc[i,"location"] = variation[1:-1]

        self.dataset = dataset

class Missense3D_data(object):

    def __init__(self, data_path="", tsv_path=""):
        self.data_path = data_path
        self.tsv_path = tsv_path


        try:
            self.load_dataset()
        except:
            self.read_tsv()


    def load_dataset(self):

        self.dataset = pd.read_csv(self.data_path, header=0, index_col=False)

    def save_dataset(self):

        self.dataset.to_csv(self.data_path, index=False)

        print("Dataset saved as: " + self.data_path)

    def read_tsv(self):

        print("No precomputed database detected, searching for TSV files")

        dataset = pd.read_csv(self.tsv_path, sep='\t', header=0, index_col=False)

        #Remove errors from dataset

        count = 0

        for i in range(dataset.shape[0]):
            if dataset.loc[i, "#UniProt ID"][0] == "#":
                dataset.drop(i, inplace=True)
                count = count + 1
        dataset.reset_index(inplace=True)

        print("--- Removed {} errors from Missense3d results ---".format(count))

        #Extract discription headers

        descriptions = dataset.loc[1, "#Description"]

        descriptions = descriptions.split("|")

        headers = []

        for i in range(16):
            headers.append(descriptions[i].split(":")[1])

        #Save prediction and description information

        for i in range(dataset.shape[0]):
            descriptions = dataset.loc[i, "#Description"]

            descriptions = descriptions.split("|")

            bool_list = [0] *  16

            if dataset.loc[i,"#Prediction"].split()[1] == "Damaging":
                dataset.loc[i, "BoolPrediction"] = 1
            else:
                dataset.loc[i, "BoolPrediction"] = 0

            for j in range(16):
                description = descriptions[j].split(":")[2]
                if description[0] == "Y":
                    dataset.loc[i, headers[j]] = 1
                else:
                    dataset.loc[i, headers[j]] = 0

        self.dataset = dataset

        print("Constructed database")

def Missense3D_training_data():

    data1 = pd.read_excel("/project/home/student1/FYP/data/raw/missense3d/all_dataset.xlsx", header=0, indexes=True)
    data2 = pd.read_excel("/project/home/student1/FYP/data/raw/missense3d/control_dataset.xlsx", header=0, indexes=True)

    data = pd.concat([data1, data2])

    data.reset_index(drop=True, inplace=True)

    return data

class FoldX(object):

    def __init__(self, pdb_id, mode=None, mutation=None):
        self.output_file = pdb_id + "_Repair_0_ST.fxout"
        self.repaired_id = pdb_id + "_Repair.pdb"
        self.position_scan_file = "PS_" + self.repaired_id[:-4] + "_scanning_output.txt"
        self.pdb_id = pdb_id + ".pdb"
        self.pdb_dir = "/project/home/student1/FYP/files/pdb/"
        self.repaired_dir = "/project/home/student1/FYP/files/repaired_pdb"
        self.output_dir = "/project/home/student1/FYP/files/foldx_stability"
        self.position_scan_dir = "/project/home/student1/FYP/files/foldx_position_scan"
        self.mutation = mutation

        if mode == "stability":
            self.stability()
        elif mode == "position_scan":
            self.position_scan()
        else:
            print("Error: No mode selected")
            exit()


    def stability(self):

        try:
            self.load_stability_output()
        except:
            os.system("module load foldx")
            try:
                self.run_stability()
                self.load_stability_output()
            except:
                self.repair_pdb()
                self.run_stability()
                self.load_output()

    def position_scan(self):

        try:
            self.run_position_scan()
            self.read_position_scan()
        except:
            self.repair_pdb()
            self.run_position_scan()
            self.read_position_scan()

    def run_position_scan(self):

        os.system("module load foldx")

        os.system("foldx --command=PositionScan --out-pdb=false --pdb-dir={} --pdb={} --output-dir={} --positions={}".format(
                                                                        self.repaired_dir,
                                                                        self.repaired_id,
                                                                        self.position_scan_dir,
                                                                        self.mutation))

        #print("Run FoldX point mutation for " + self.pdb_id + " with mutation " + self.mutation)

    def read_position_scan(self):

        try:
            #Read and extract ddG calculation
            output = open(self.position_scan_dir + "/" + self.position_scan_file, "r")
            self.ddG = float(output.readlines()[1][8:])
        except:
            pass

    def load_stability_output(self):

        #Read and extract stability calculation
        output = open(self.output_dir + "/" + self.output_file, "r")
        output = output.read()
        output = output.split("\t")

        self.stability = float(output[1])

    def repair_pdb(self):

        os.system("foldx --command=RepairPDB --pdb-dir={} --pdb={} --output-dir={}".format(
                                                                        self.pdb_dir,
                                                                        self.pdb_id,
                                                                        self.repaired_dir))

        print("Repaired " + self.pdb_id)

    def run_stability(self):

        shell_cmd = ("foldx --command=Stability --pdb-dir={} --pdb={} --output-dir={}".format(
                                                                        self.repaired_dir,
                                                                        self.repaired_id,
                                                                        self.output_dir))

        os.system(shell_cmd)

        #print("Run FoldX stability calculations for " + self.pdb_id)

def read_dssp(dsspfile):

    #Read DSSP file
    dsspfile =  open(dsspfile, "r")
    lines = dsspfile.readlines()

    for i, line in enumerate(lines):
        if line[2] == "#":
            start = i

    lines = lines[start+1:]

    #Extract ASA information
    asa_dict = {}

    for line in lines:

        try:


            res_id = int(line[7:10].strip())
            """
            print(res_id)

            for i in range(len(res_id)):
                print(res_id[i])
                if res_id[i] != " ":
                    res_id = int(res_id[i:])
            """
            asa = int(line[36:38])
            asa_dict["res_" + str(res_id)] = asa
        except:
            pass

    return asa_dict

def get_ASA(pdb_id, position):

    pdbfile = "/project/home/student1/FYP/files/pdb/" + pdb_id + ".pdb"
    dsspfile = "/project/home/student1/FYP/files/dssp/" + pdb_id + ".dssp"
    logfile = "/project/home/student1/FYP/files/dssp/" + pdb_id + ".log"

    shell_cmd = ("dssp {} {} > {} ".format(pdbfile, dsspfile, logfile))

    os.system(shell_cmd)

    shell_check = os.system("echo $?")


    if shell_check != 0:
        print("DSSP Error detected for " + pdb_id)

    asa_dict = read_dssp(dsspfile)



    return asa_dict["res_" + str(position)]
