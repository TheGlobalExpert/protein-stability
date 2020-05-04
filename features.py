import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
from tools import Master_results
import math

data = Master_results()
print(data)

labels = "Disulphide breakage,Buried Pro introduced,Clash,Buried hydropilic introduced,Buried charge introduced,Secondary structure altered,Buried charge switch,Disallowed phi/psi,Buried charge replaced,Buried Gly replaced,Buried H-bond breakage,Buried salt bridge breakage,Cavity altered,Buried / exposed switch,Cis pro replaced,Gly in a bend".split(",")

thresholds = [1.0, 1.5 ,2.0]

plot_threshold = False
plot_combined = False
plot_abs = True

def plot_bar_chart(threshold, data):

    for i in range(data.shape[0]):

        ddG = data.loc[i, "ddG"]

        try:
            ddG = ddG.iloc[0]
        except:
            pass
        print(ddG)
        """
        if ddG[-1] == ")":
            ddG = ddG[:-3]
        """
        try:
            ddG = float(ddG)

            if ddG >= threshold:
                data.loc[i, "true_damage"] = 1
            elif ddG < threshold:
                data.loc[i, "true_damage"] = 0
        except:
            data.drop(i)
            exit()

    data.info()
    positive = []
    negative = []

    for i in range(data.shape[0]):
        print(i)
        print([char for char in data.loc[i, "one_hot_features"]][:-1])
        features = np.array([char for char in data.loc[i, "one_hot_features"]][:-1]).astype(np.float)
        print(features)

        if data.loc[i, "true_damage"] == 1.0:
            positive.append(features)
        elif data.loc[i, "true_damage"] == 0.0:
            negative.append(features)

    positive = np.stack(positive)
    negative = np.stack(negative)
    print(negative)
    print(positive.shape)
    print(negative.shape)

    np.sum(positive, axis=0)

    TPR = np.sum(positive, axis=0)/positive.shape[0]
    FPR = np.sum(negative, axis=0)/negative.shape[0]
    n_positive = positive.shape[0]
    n_negative = negative.shape[0]
    abs_postive = np.sum(positive, axis=0)
    abs_negative = np.sum(negative, axis=0)

    ratios = TPR/FPR


    barWidth = 0.4
    r1 = np.arange(len(TPR))
    r2 = [x + barWidth for x in r1]
    if plot_threshold == True:
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
        plt.show()

    return ratios, TPR, FPR, n_positive, n_negative, abs_postive, abs_negative

if plot_abs == True:
    barWidth = 0.13

    colours = ["green", "blue", "red"]

    fig, ax1 = plt.subplots(figsize=(8,7))

    ax1.set_ylabel('Positive rate (%)', fontweight='bold')
    ax1.set_xticks([r + barWidth/2 for r in range(len(labels))])
    ax1.set_xticklabels(labels)
    fig.autofmt_xdate(bottom=0.2, rotation=45, ha='right')
    ax2 = ax1.twinx()

    r1 = np.arange(len(labels))
    r1 = [x - 2*barWidth for x in r1]
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]
    r4 = [x + barWidth for x in r3]
    r5 = [x + barWidth for x in r4]
    r6 = [x + barWidth for x in r5]

    x_positions = [[r1, r4], [r2, r5], [r3, r6]]

    for threshold, x_pos, colour in zip(thresholds, x_positions, colours):

        ratios, TPRs, FPRs, n_positive, n_negative, abs_postive, abs_negative = plot_bar_chart(threshold, data)

        #FPR_CI = [FPR + (1.96 * math.sqrt((FPR * (1 - FPR) / n_positive))), FPR - (1.96 * math.sqrt((FPR * (1 - FPR) / n_negative)))]

        TPR_sig = []
        FPR_sig = []

        for TPR in TPRs:

            TPR_CI = [TPR + (1.96 * math.sqrt((TPR * (1 - TPR) / n_positive))), TPR - (1.96 * math.sqrt((TPR * (1 - TPR) / n_positive)))]
            if TPR < TPR_CI[0] and TPR > TPR_CI[1]:
                TPR_sig.append(True)
            else:
                TPR_sig.append(False)

        for FPR in FPRs:

            FPR_CI = [FPR + (1.96 * math.sqrt((FPR * (1 - FPR) / n_positive))), FPR - (1.96 * math.sqrt((FPR * (1 - FPR) / n_negative)))]
            if FPR < FPR_CI[0] and FPR > FPR_CI[1]:
                FPR_sig.append(True)
            else:
                FPR_sig.append(False)

        ax1.bar(x_pos[0], abs_postive, align='center', alpha=1, width=barWidth, edgecolor='white', color=colour, label=str(threshold))
        ax1.bar(x_pos[1], abs_negative, align='center', alpha=0.5, width=barWidth, edgecolor='white', color=colour)

        ax1.set_ylabel('Absolute positives', fontweight='bold')
        ax1.set_xticks([r + barWidth/2 for r in range(len(FPRs))])
        ax1.set_xticklabels(labels, fontsize=10)
        fig.autofmt_xdate(bottom=0.2, rotation=45, ha='right')


        ax2.plot([r + barWidth/2 for r in range(len(FPRs))], ratios, color=colour, label="Ratio", alpha=0.5)
        ax2.set_ylabel('TPR/FPR ratio', fontweight='bold', rotation=270, labelpad=13)

        marker_x = [r + barWidth/2 for r in range(len(FPRs))]

        print(FPR_sig)
        print(TPR_sig)

        for i, ratio in enumerate(ratios):
            if FPR_sig[i] == True and TPR_sig[i] == True:
                ax2.scatter(marker_x[i], ratio)
                ax2.text(marker_x[i], ratio, str(round(ratio, 1)),
                         bbox={'facecolor': 'white', 'alpha': 0.2, 'edgecolor': 'black', 'pad': 1.5}, ha='center',
                         va='center')

        """
        for i, ratio in enumerate(ratios):
            ax2.text(marker_x[i], ratio, str(round(ratio,1)),
                bbox={'facecolor':'white','alpha':0.2,'edgecolor':'black','pad':1.5}, ha='center', va='center')
        """

    ax1.text(15, 42, "Solid bar = True Positives\nLight bar = False Positives", ha='center', va='center')
    ax2.set_ylim(bottom=0)
    plt.title("Absolute number of structural features observed (HotMusic dataset)")
    leg = ax1.legend(loc=2, title="\u0394\u0394G threshold\n    (kcal/mol)")
    #leg._legend_box.align = "right"
    fig.tight_layout()
    plt.show()





if plot_combined == True:

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
