from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np
import sys

def odds_to_prob(odds_in):
    if odds_in<0:
        return( (-1*(odds_in)) / (-1*(odds_in) + 100))
    elif odds_in>0:
        return(100 / (odds_in + 100))
    else:
        print("PROBLEM")






def make_html_file(filename, calibration_file="", roc_file="",pr_file=""):
    with open(filename, "w") as record_file:
        record_file.write('<!DOCTYPE html>\n')
        record_file.write('<html lang="en">\n')
        record_file.write('<head>\n')
        record_file.write("<title>Mike's Website</title>\n")
        record_file.write('</head>\n')
        record_file.write('<body>\n')
        record_file.write('<div>\n')
        record_file.write(f'<img src = "{calibration_file}" width = "40%"  >\n')
        record_file.write('</div>\n')
        record_file.write('<div>\n')
        record_file.write(f'<img src = "{roc_file}" width = "40%"  >\n')

        record_file.write('</div>\n')
        record_file.write('<div>\n')
        record_file.write(f'<img src = "{pr_file}" width = "40%"  >\n')

        record_file.write('</div>\n')
        record_file.write('</body>\n')
        record_file.write('<head>\n')
        record_file.write('</html>\n')








def calibration_plot(y_true,y_score,show=1, savefile="", title=""):

    assert len(y_true) == len(y_score)




    print("in ujs function")

    bin_bounds = [0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]

    # bin_bounds = [0,0.2,0.4,0.6,0.8,1]

    error = 0

    bin_means = []
    outcome_means = []
    outcome_stds = []


    for i in range(len(bin_bounds)-1):

        total = 0
        happened = 0

        outcomes = []

        for j in range(len(y_score)):

            score = y_score[j]

            if score >= bin_bounds[i] and score < bin_bounds[i+1]:


                total += 1

                happened += y_true[j]
                outcomes.append(y_true[j])

        bin_means.append(np.mean([bin_bounds[i],bin_bounds[i+1]]))
        outcome_means.append(np.mean(outcomes))
        outcome_stds.append(np.std(outcomes))

    print(len(bin_means))
    print(len(outcome_means))


    print(outcome_means)

    plt.scatter(bin_means, outcome_means)
    # plt.errorbar(bin_means, outcome_means, yerr=outcome_stds, fmt="o")

    plt.xlabel("Prediction Probability",fontsize=14)
    plt.ylabel("Outcome Fraction",fontsize=14)
    plt.ylim(0,1)
    plt.xlim(0,1)
    plt.title(title, fontsize=14)

    perfect, = plt.plot([0,1],[0,1],color="black",label="perfect")

    plt.legend(handles=[perfect],fontsize=14,)




    if len(savefile)>0:
        plt.savefig(savefile)

    if show:
        plt.show()





    plt.close()







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

    brier = brier_score(y_true,y_score)

    if round:
        auroc = np.round(auroc,decimals=3)
        ns_auroc = np.round(ns_auroc,decimals=3)
        aupr = np.round(aupr,decimals=3)
        ns_aupr = np.round(ns_aupr,decimals=3)
        brier = np.round(brier,decimals=3)




    ##print stats
    print()
    print()
    print("Brier score:")
    print(brier)    
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



def plot_roc_curve(y_true,y_score, show=1, savefile="", title=""):

    if sum(y_true)/len(y_true) >=0.5:
        y_ns = [1 for _ in range(len(y_true))]
    else:
        y_ns = [0 for _ in range(len(y_true))]


    fpr, tpr, roc_thresholds = metrics.roc_curve(y_true, y_score, pos_label=1)
    skill_plot, = plt.plot(fpr,tpr,label="Model",color="blue")

    ns_fpr, ns_tpr, ns_roc_thresholds = metrics.roc_curve(y_true, y_ns, pos_label=1)
    noskill_plot, = plt.plot(ns_fpr,ns_tpr,label="No Skill",color="red")

    plt.legend(handles=[skill_plot, noskill_plot],fontsize=14,)
    plt.xlabel("False Positive Rate",fontsize=14)
    plt.ylabel("True Positive Rate",fontsize=14)
    plt.ylim(0,1)
    plt.xlim(0,1)
    plt.title(title, fontsize=14)


    if len(savefile)>0:
        plt.savefig(savefile)

    if show:
        plt.show()

    plt.close()





def plot_pr_curve(y_true,y_score, show=1, savefile="", title=""):

    if sum(y_true)/len(y_true) >=0.5:
        ns_aupr = sum(y_true) / len(y_true)
    else:
        ns_aupr = 1 - sum(y_true) / len(y_true)

    precision, recall, thresholds = metrics.precision_recall_curve(y_true, y_score)

    skill_plot, = plt.plot(recall,precision,label="Model",color="blue")

    noskill_plot = plt.axhline(y=ns_aupr,label="No Skill",color="red")

    plt.legend(handles=[skill_plot, noskill_plot],fontsize=14,)
    plt.xlabel("Recall",fontsize=14)
    plt.ylabel("Precision",fontsize=14)
    plt.ylim(0,1)
    plt.xlim(0,1)
    plt.title(title, fontsize=14)


    if len(savefile)>0:
        plt.savefig(savefile)

    if show:
        plt.show()

    plt.close()