from Bio.PDB.PDBExceptions import PDBConstructionWarning
from Bio.PDB import *
from Bio.Data.IUPACData import protein_letters_3to1
from Bio.PDB.DSSP import DSSP
import numpy as np
import math
import os, sys

def calculate_distance(res1, res2):  #Calculates the Euclidian distance between two residues
    return math.sqrt(np.sum((np.array(res1) - np.array(res2))**2))

def res_in_range(pdb_id, position, distance):
    # Returns a 20x1 np array containing the number of
    # each type of residues within a certain radius of the ROI
    fullfilename = "files/pdb/" + pdb_id + ".pdb"
    structure = PDBParser().get_structure(pdb_id.upper(), fullfilename)

    res_dict ={}

    print(pdb_id)

    for model in structure:
        for chain in model:
            for residue in chain:
                if is_aa(residue, standard=True): # Check if amino acid
                    for atom in residue:
                        if atom.get_name() == "CA":

                            #Get, reformat and store residue type
                            resname = residue.get_resname()
                            first_resname = resname[0]
                            resname = first_resname + resname[1:3].lower()
                            resname = protein_letters_3to1[resname]

                            res_id = "res_" + str(residue.id[1])

                            print(res_id)

                            res_dict[res_id] = {"coords" : atom.get_coord().tolist(), "type" : resname}



    AAs = ["A","R","N","D","C","E","Q","G","H","I","L","K","M","F","P","S","T","W","Y","V"]
    AA_environment = np.zeros(20)

    ROI = res_dict["res_" + str(position)]["coords"]

    for residue in res_dict:
        print(residue)
        res_distance = calculate_distance(ROI, res_dict[residue]["coords"])

        if res_distance <= distance:
            res_index = AAs.index(res_dict[residue]["type"])
            AA_environment[res_index] = AA_environment[res_index] + 1
        else:
            pass

    return AA_environment

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

            print(line[7:10].strip())
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
    print(end="\r")

    if shell_check != 0:
        print("DSSP Error detected for " + pdb_id)

    asa_dict = read_dssp(dsspfile)

    print(asa_dict)

    return asa_dict["res_" + str(position)]

#res_in_range("3uue", 20, 15)

#get_ASA("1lhm", 20)
