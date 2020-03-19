import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
import seaborn as sns; sns.set()

missense3d = np.load("results/missense3d_reduced.npy")
hotmusic = np.load("results/hotmusic_reduced.npy")

alphabet = ["Non-polar", "Polar", "-ve", "+ve", "Glycine", "Cysteine", "Proline"]


print(missense3d, hotmusic)

missense3d = missense3d/np.sum(missense3d)
hotmusic = hotmusic/np.sum(hotmusic)

corr = round(np.corrcoef(missense3d, hotmusic)[0,1],2)

print(corr)

matrix = hotmusic/missense3d

matrix = np.round(matrix,1)

print(matrix)
heat_map = sb.heatmap(matrix, cmap=sb.color_palette("coolwarm", 100000),
                    center=1,vmin=0, vmax=2.4, annot=True, square=True)

heat_map.set_xticklabels(alphabet)
heat_map.set_yticklabels(alphabet,va='center')
heat_map.set_ylabel("Wild type residue")
heat_map.set_xlabel("Mutant residue")
heat_map.set_title("Ratio between percentage occurances of mutations in the HotMusic\ndataset vs. the Missense3D dataset (Correlation coefficent = {})".format(corr))

no_data = [[6,3],[7,3],[5,5,],[7,5],[3,6],[6,6],[7,6],[3,7],[5,7],[6,7],[7,7]]

for point in no_data:
    text = heat_map.text(point[0]-0.5, point[1]-0.5, "No\ndata",
                   ha="center", va="center", color="black")


plt.show()
