import sys
import numpy as np 
import csv
from sklearn import metrics
import matplotlib.pyplot as plt
from eval_functions import *


## data source:
#https://www.sportsbookreviewsonline.com/scoresoddsarchives/ncaabasketball/ncaabasketballoddsarchives.htm







data = []
## read CSV / TSV
with open("data/ncaa_football_2021-22.csv") as tsvfile:
    spamreader = csv.reader(tsvfile, delimiter=',')

    next(spamreader)
    for row in spamreader:
        try:
            data.append([row[0], row[2], row[3], float(row[6]),float(row[9]) ])
        except:
            pass
        # Date, VH, Team, Final score, ML odds, 
        # try/except to avoid nolines (when no moneyline bet is listed)
        # input()



y_true = []
# did home team win?

y_score = []

for i in range(0,len(data), 2):

    if data[i][1]!="N":
        # avoiding neutral games, only looking at ones where one team is home and other is away
        try:
            assert(data[i][0] == data[i+1][0])
            assert(data[i][1] != data[i+1][1])
            assert( data[i+1][1]=="H")
        except:
            print(data[i])
            print(data[i+1])
            input()

        v_score = data[i][3]
        h_score = data[i+1][3]

        oddsV = data[i][4]
        oddsH = data[i+1][4]

        probV = odds_to_prob(oddsV)
        probH = odds_to_prob(oddsH)


        # print(probV+probH)


        if v_score==h_score:
            print("TIE!!!!!")

        elif h_score>v_score:
            y_true.append(1)
            y_score.append(probH)

        else:
            y_true.append(0)
            y_score.append(probH)


print(len(y_true))
print(len(y_score))


y_ns = [1 for _ in range(len(y_true))]


# ## ROC curve
fpr, tpr, roc_thresholds = metrics.roc_curve(y_true, y_score, pos_label=1)

auroc = metrics.roc_auc_score(y_true, y_score)
# print(auroc)
plt.plot(fpr,tpr)


fpr, tpr, roc_thresholds = metrics.roc_curve(y_true, y_ns, pos_label=1)

ns_auroc = metrics.roc_auc_score(y_true, y_ns)
# print(auroc)


plt.plot(fpr,tpr)
plt.show()




precision, recall, thresholds = metrics.precision_recall_curve(y_true, y_score)
# plt.plot(recall,precision)


aupr = metrics.auc(recall,precision)

ns_aupr = sum(y_true) / len(y_true)

# plt.axhline(y=ns_aupr)
# print(aupr)
# print(noskill_aupr)
# plt.show()



##print stats
print("AUROC:")
print(auroc)
print("NS AUROC:")
print(ns_auroc)
print()
print("AUPR:")
print(aupr)
print("NS AUPR:")
print(ns_aupr)