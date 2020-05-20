import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
import seaborn as sns; sns.set()

missense3d = np.load("results/missense3d_reduced.npy")
hotmusic = pd.read_csv("results/master.csv")

alphabet = ["Non-polar", "Polar", "-ve", "+ve", "Glycine", "Cysteine", "Proline"]

alphabet_dict = {"A" : "Non-polar", "V" : "Non-polar", "L" : "Non-polar", "I" : "Non-polar", "M" : "Non-polar", "W" : "Non-polar", "F" : "Non-polar",
                    "S" : "Polar", "T" : "Polar", "Y" : "Polar", "N" : "Polar", "Q" : "Polar",
                    "D" : "-ve", "E" : "-ve",
                    "K" : "+ve", "R" : "+ve", "H" : "+ve",
                    "G" : "Glycine", "C" : "Cysteine", "P" : "Proline"}

hotmusic_matrix = np.zeros([7,7])

#----Calculate HotMusic heatmap----#

for i in range(hotmusic.shape[0]):

    wt = hotmusic.loc[i, "wt"]
    mut = hotmusic.loc[i, "mut"]

    wt = alphabet.index(alphabet_dict[wt])
    mut = alphabet.index(alphabet_dict[mut])

    hotmusic_matrix[wt, mut] += 1

#----Prepare and render heatmap----#

print(hotmusic_matrix)

print(np.sum(missense3d))
print(np.sum(hotmusic_matrix))

missense3d = missense3d/np.sum(missense3d)
hotmusic_matrix = hotmusic_matrix/np.sum(hotmusic_matrix)

corr = round(np.corrcoef(missense3d, hotmusic_matrix)[0,1],2)

print(corr)

print(missense3d)
print(hotmusic_matrix)

matrix = hotmusic_matrix/missense3d

matrix = np.round(matrix,1)

print(matrix)
heat_map = sb.heatmap(matrix, cmap=sb.color_palette("coolwarm", 100000),
                    center=1,vmin=0, vmax=4, annot=True, square=True)

heat_map.set_xticklabels(alphabet)
heat_map.set_yticklabels(alphabet,va='center')
heat_map.set_ylabel("Wild type residue")
heat_map.set_xlabel("Mutant residue")
#heat_map.set_title("Ratio between percentage occurances of mutations in the HotMusic\ndataset vs. the Missense3D dataset (Correlation coefficent = {})".format(corr))

no_data = [[6,3],[7,3],[5,5,],[7,5],[3,6],[6,6],[7,6],[3,7],[5,7],[6,7],[7,7]]

for point in no_data:
    text = heat_map.text(point[0]-0.5, point[1]-0.5, "No\ndata",
                   ha="center", va="center", color="black")


plt.show()
