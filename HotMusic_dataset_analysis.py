from tools import HotMusic_data, Missense3D_training_data
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import seaborn as sb
from Bio.Data.IUPACData import protein_letters_3to1


data = HotMusic_data(data_path="data/HotMusic_Charlie_doubles_removed.csv").dataset

AAs = ["A","V","L","I","M","W","F", #Non-Polar
    "S","T","Y","N","Q", #Polar
    "D","E", #Negative
    "K","R","H", #Positive
    "G","C","P"] #Specials

alphabet_dict = {"A" : "Non-polar", "V" : "Non-polar", "L" : "Non-polar", "I" : "Non-polar", "M" : "Non-polar", "W" : "Non-polar", "F" : "Non-polar",
                    "S" : "Polar", "T" : "Polar", "Y" : "Polar", "N" : "Polar", "Q" : "Polar",
                    "D" : "-ve", "E" : "-ve",
                    "K" : "+ve", "R" : "+ve", "H" : "+ve",
                    "G" : "Glycine", "C" : "Cysteine", "P" : "Proline"}

alphabet = ["Non-polar", "Polar", "-ve", "+ve", "Glycine", "Cysteine", "Proline"]

#FULL ALPHABET

matrix = np.zeros((20,20))

for i in range(data.shape[0]):
    wt = data.loc[i, "wt"]
    mut = data.loc[i, "mut"]
    wt_index = AAs.index(wt)
    mut_index = AAs.index(mut)

    matrix[wt_index,mut_index] += 1

print(matrix)

"""

fig, ax = plt.subplots()
im = ax.imshow(matrix, cmap='hot')#, ='nearest')


ax.set_xticks(np.arange(len(AAs)))
ax.set_yticks(np.arange(len(AAs)))

ax.set_xticklabels(AAs)
ax.set_yticklabels(AAs)
ax.set_ylabel("Mild type residue")
ax.set_xlabel("Mutant residue")


for i in range(len(AAs)):
    for j in range(len(AAs)):
        text = ax.text(j, i, int(matrix[i, j]),
                       ha="center", va="center", color="w")
text = ax.text(0, 1, int(matrix[1, 0]),
               ha="center", va="center", color="black")

ax.set_title("Mutation matrix of HotMusic dataset\nwith whole amino acid alphabet (n = {})".format(int(data.shape[0])))
ax.set_aspect(1)
fig.tight_layout()
plt.show()


"""

matrix = np.zeros((7,7))

for i in range(data.shape[0]):
    wt = data.loc[i, "wt"]
    mut = data.loc[i, "mut"]
    wt_index = alphabet.index(alphabet_dict[wt])
    mut_index = alphabet.index(alphabet_dict[mut])

    matrix[wt_index,mut_index] += 1

print(matrix)
print(len(alphabet))

def reduced_heatmap(matrix, title):

    size = int(data.shape[0])

    fig, ax = plt.subplots()
    im = ax.imshow(matrix, cmap='hot')#, ='nearest')


    ax.set_xticks(np.arange(len(alphabet)))
    ax.set_yticks(np.arange(len(alphabet)))

    ax.set_xticklabels(alphabet)
    ax.set_yticklabels(alphabet)
    ax.set_ylabel("Mild type residue")
    ax.set_xlabel("Mutant residue")


    for i in range(len(alphabet)):
        for j in range(len(alphabet)):
            text = ax.text(j, i, str(int(matrix[i, j])) + "\n" + str(round(int(100*matrix[i, j])/size,2)) + "%",
                           ha="center", va="center", color="w")
            """
            text = ax.text(j, i, str(int(matrix[i, j])),
                           ha="center", va="center", color="w")
            """

    text = ax.text(0, 0, str(int(matrix[0, 0])) + "\n" + str(round(int(100*matrix[0, 0])/size,2)) + "%",
                   ha="center", va="center", color="black")

    ax.set_title(title + " (n = {})".format(int(data.shape[0])))
    ax.set_aspect(1)
    fig.tight_layout()
    plt.show()


reduced_heatmap(matrix,"Mutation matrix of HotMusic dataset with\nreduced amino acid alphabet")

np.save("results/hotmusic_reduced.npy", matrix)

data = Missense3D_training_data()
print(data)
matrix = np.zeros((7,7))

for i in range(data.shape[0]):
    wt = data.loc[i, "#Orig Amino Acid"]
    wt_1 = wt[0]
    wt = wt_1 + wt[1:].lower()
    wt = protein_letters_3to1[wt]
    mut = data.loc[i, "#Mutant Amino Acid"]
    print(mut)
    mut_1 = mut[0]
    mut = mut_1 + mut[1:].lower()
    mut = protein_letters_3to1[mut]
    wt_index = alphabet.index(alphabet_dict[wt])
    mut_index = alphabet.index(alphabet_dict[mut])

    matrix[wt_index,mut_index] += 1

reduced_heatmap(matrix, "Mutation matrix of Missense3D training\ndataset with reduced amino acid alphabet")

np.save("results/missense3d_reduced.npy", matrix)
