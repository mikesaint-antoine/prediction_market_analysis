from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np

def odds_to_prob(odds_in):
    if odds_in<0:
        return( (-1*(odds_in)) / (-1*(odds_in) + 100))
    elif odds_in>0:
        return(100 / (odds_in + 100))
    else:
        print("PROBLEM")





def brier_score(y_true,y_score):


    assert len(y_true) == len(y_score)


    N = len(y_score)

    total = 0

    for i in range(N):
        total += (y_score[i] - y_true[i])**2

    total = total/N



    return total





def print_stats(y_true,y_score, round=0):
    


    auroc = metrics.roc_auc_score(y_true, y_score)

    if sum(y_true)/len(y_true) >=0.5:
        y_ns = [1 for _ in range(len(y_true))]
        ns_aupr = sum(y_true) / len(y_true)
    else:
        y_ns = [0 for _ in range(len(y_true))]
        ns_aupr = 1 - sum(y_true) / len(y_true)

    ns_auroc = metrics.roc_auc_score(y_true, y_ns)

    precision, recall, thresholds = metrics.precision_recall_curve(y_true, y_score)

    aupr = metrics.auc(recall,precision)

    if round:
        auroc = np.round(auroc,decimals=3)
        ns_auroc = np.round(ns_auroc,decimals=3)
        aupr = np.round(aupr,decimals=3)
        ns_aupr = np.round(ns_aupr,decimals=3)




    ##print stats
    print()
    print()
    print("AUROC:")
    print(auroc)
    print("NS AUROC:")
    print(ns_auroc)
    print()
    print("AUPR:")
    print(aupr)
    print("NS AUPR:")
    print(ns_aupr)



def plot_roc_curve(y_true,y_score, show=1, savefile=""):

    if sum(y_true)/len(y_true) >=0.5:
        y_ns = [1 for _ in range(len(y_true))]
    else:
        y_ns = [0 for _ in range(len(y_true))]


    fpr, tpr, roc_thresholds = metrics.roc_curve(y_true, y_score, pos_label=1)
    skill_plot, = plt.plot(fpr,tpr,label="Model",color="blue")

    ns_fpr, ns_tpr, ns_roc_thresholds = metrics.roc_curve(y_true, y_ns, pos_label=1)
    noskill_plot, = plt.plot(ns_fpr,ns_tpr,label="No Skill",color="red")

    plt.legend(handles=[skill_plot, noskill_plot],fontsize=14,)
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.ylim(0,1)
    plt.xlim(0,1)


    if len(savefile)>0:
        plt.savefig(savefile)

    if show:
        plt.show()

    plt.close()





def plot_pr_curve(y_true,y_score, show=1, savefile=""):

    if sum(y_true)/len(y_true) >=0.5:
        ns_aupr = sum(y_true) / len(y_true)
    else:
        ns_aupr = 1 - sum(y_true) / len(y_true)

    precision, recall, thresholds = metrics.precision_recall_curve(y_true, y_score)

    skill_plot, = plt.plot(recall,precision,label="Model",color="blue")

    noskill_plot = plt.axhline(y=ns_aupr,label="No Skill",color="red")

    plt.legend(handles=[skill_plot, noskill_plot],fontsize=14,)
    plt.xlabel("Recall")
    plt.ylabel("Precision")
    plt.ylim(0,1)
    plt.xlim(0,1)


    if len(savefile)>0:
        plt.savefig(savefile)

    if show:
        plt.show()

    plt.close()