import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data1 = pd.read_csv("data/processed_hotmusic.csv")
data2 = pd.read_csv("data/processed_missense.csv")

data1.set_index("mut_info", inplace=True)

labels = "Disulphide breakage,Buried Pro introduced,Clash,Buried hydropilic introduced,Buried charge introduced,Secondary structure altered,Buried charge switch,Disallowed phi/psi,Buried charge replaced,Buried Gly replaced,Buried H-bond breakage,Buried salt bridge breakage,Cavity altered,Buried / exposed switch,Cis pro replaced,Gly in a bend".split(",")

def plot_bar_chart(threshold):

    for i in range(data2.shape[0]):
        mut_info = data2.loc[i,"mut_info"]

        ddG = data1.loc[mut_info, "ddG"]

        if ddG[-1] == ")":
            ddG = ddG[:-3]

        try:
            ddG = float(ddG)

            if ddG >= threshold:
                data2.loc[i, "true_damage"] = 1
            elif ddG < threshold:
                data2.loc[i, "true_damage"] = 0
        except:
            data2.drop(i)

    data2.reset_index()

    data = data2[data2.columns[13:]]

    changes = []

    for i in range(data.shape[0]):
        if data.loc[i, "true_damage"] == 1.0:

            changes.append(np.array(data.loc[i, data.columns[:-1]]).reshape(16,1))


    data = np.stack(changes)

    data = data.reshape(data.shape[:2])

    print(data)
    print(data.shape)

    total = data.shape[0]

    counts = np.sum(data, axis=0)/total

    print(len(counts))
    print(len(labels))

    y_pos = np.arange(len(labels))
    plt.barh(y_pos, counts, align='center', alpha=0.5)
    plt.yticks(y_pos, labels)
    plt.ylabel('Usage')
    plt.title('Programming language usage')

    plt.show()
plot_bar_chart(2)
