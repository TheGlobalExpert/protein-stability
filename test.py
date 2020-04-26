import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

data1 = pd.read_csv("data/processed_hotmusic.csv")
data2 = pd.read_csv("data/processed_missense.csv")

data1.set_index("mut_info", inplace=True)

labels = "Disulphide breakage,Buried Pro introduced,Clash,Buried hydropilic introduced,Buried charge introduced,Secondary structure altered,Buried charge switch,Disallowed phi/psi,Buried charge replaced,Buried Gly replaced,Buried H-bond breakage,Buried salt bridge breakage,Cavity altered,Buried / exposed switch,Cis pro replaced,Gly in a bend".split(",")

def plot_bar_chart(threshold):

    for i in range(data2.shape[0]):
        mut_info = data2.loc[i,"mut_info"]

        ddG = data1.loc[mut_info, "ddG"]


        try:
            ddG = ddG.iloc[0]
        except:
            pass


        if ddG[-1] == ")":
            ddG = ddG[:-3]
        print(ddG)


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
    print(data)

    positive = []
    negative = []

    for i in range(data.shape[0]):
        if data.loc[i, "true_damage"] == 1.0:
            positive.append(np.array(data.loc[i, data.columns[:-1]]).reshape(16,1))
        elif data.loc[i, "true_damage"] == 0.0:
            negative.append(np.array(data.loc[i, data.columns[:-1]]).reshape(16,1))

    positive = np.stack(positive)
    positive = positive.reshape(positive.shape[:2])
    negative = np.stack(negative)
    negative = negative.reshape(negative.shape[:2])


    TPR = 100*np.sum(positive, axis=0)/positive.shape[0]
    FPR = 100*np.sum(negative, axis=0)/negative.shape[0]
    print(positive.shape[0])
    print(negative.shape[0])

    ratios = TPR/FPR


    barWidth = 0.4
    r1 = np.arange(len(TPR))
    r2 = [x + barWidth for x in r1]
    """
    fig, ax1 = plt.subplots(figsize=(8,7))


    ax1.bar(r1, TPR, align='center', alpha=0.5, width=barWidth, edgecolor='white', label='TPR')
    ax1.bar(r2, FPR, align='center', alpha=0.5, width=barWidth, edgecolor='white', label='FPR')

    ax1.set_ylabel('Positive rate (%)', fontweight='bold')
    ax1.set_xticks([r + barWidth/2 for r in range(len(FPR))])
    ax1.set_xticklabels(labels)
    fig.autofmt_xdate(bottom=0.2, rotation=45, ha='right')

    ax2 = ax1.twinx()
    ax2.plot([r + barWidth/2 for r in range(len(FPR))], ratios, color="black", label="Ratio", marker="s", markerfacecolor="white")
    ax2.set_ylabel('TPR/FPR ratio', fontweight='bold', rotation=270, labelpad=13)

    marker_x = [r + barWidth/2 for r in range(len(FPR))]
    for i, ratio in enumerate(ratios):
        ax2.text(marker_x[i], ratio, str(round(ratio,1)),
            bbox={'facecolor':'white','alpha':1,'edgecolor':'black','pad':1.5}, ha='center', va='center')


    plt.title('Threshold = ' + str(threshold))
    fig.legend(loc=4)
    fig.tight_layout()
    #plt.show()
    """
    return ratios

thresholds = [1.0, 1.5 ,2.0]
colours = ["green", "orange", "red"]
plot_bools = [False, True, False, True, False, False, False, False, False, False, False, False, False, False, True, False]
barWidth = 0.4

fig, ax1 = plt.subplots(figsize=(5,4))
ax1.set_xticks([r + barWidth/2 for r in range(16)])
ax1.set_xticklabels(labels)
fig.autofmt_xdate(bottom=0.2, rotation=60, ha='right')


for threshold, colour in zip(thresholds, colours):
    ratios = plot_bar_chart(threshold)

    ax1.plot([r + barWidth/2 for r in range(len(ratios))], ratios, color=colour, label=str(threshold), marker="s", markerfacecolor="white")
    ax1.set_ylabel('TPR/FPR ratio', fontweight='bold', labelpad=13)


    marker_x = [r + barWidth/2 for r in range(len(ratios))]
    for i, ratio in enumerate(ratios):
        if plot_bools[i] == True:
            ax1.text(marker_x[i], ratio, str(round(ratio,1)),
                bbox={'facecolor':'white','alpha':1,'edgecolor':colour,'pad':1.5}, ha='center', va='center')


print(r"\u0394")
ax1.set_ylim(bottom=0)
leg = ax1.legend(loc=1, title="\u0394\u0394G threshold\n   (kcal/mol)")
leg._legend_box.align = "right"
fig.tight_layout()
plt.show()
