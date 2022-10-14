import sys
import numpy as np 
import csv
# from sklearn import metrics
import matplotlib.pyplot as plt
from eval_functions import *




## data source:
# https://sportsbookreviewsonline.com/scoresoddsarchives/mlb/mlboddsarchives.htm







# print(odds_to_prob(190))
# print(odds_to_prob(-210))



# print("test")


data = []
## read CSV / TSV
with open("data/mlb_2021.csv") as tsvfile:
    spamreader = csv.reader(tsvfile, delimiter=',')

    next(spamreader)
    for row in spamreader:
        data.append([row[0],row[2], row[3], float(row[14]), float(row[15]),float(row[16])])
        # Date, VH, Team, Final score, Odds open, Odds close




y_true = []
# did home team win?

y_open = []
y_close = []

for i in range(0,len(data), 2):
    assert(data[i][0] == data[i+1][0])
    assert(data[i][1] != data[i+1][1])
    assert( data[i+1][1]=="H")


    v_score = data[i][3]
    h_score = data[i+1][3]


    odds1_open = data[i][4]
    odds1_close = data[i][5]


    odds2_open = data[i+1][4]
    odds2_close = data[i+1][5]


    prob1_open = odds_to_prob(odds1_open)
    prob1_close = odds_to_prob(odds1_close)

    prob2_open = odds_to_prob(odds2_open)
    prob2_close = odds_to_prob(odds2_close)


    if v_score==h_score:
        print("TIE!!!!!")

    elif h_score>v_score:
        y_true.append(1)
        y_open.append(prob2_open)
        # y_open.append(prob2_open / (prob1_open+prob2_open))


        y_close.append(prob2_close)

    else:
        y_true.append(0)
        y_open.append(prob2_open)
        # y_open.append(prob2_open / (prob1_open+prob2_open))

        y_close.append(prob2_close)

    # odds1 = data[i][5]
    # odds2 = data[i+1][5]

    # prob1 = odds_to_prob(odds1)
    # prob2 = odds_to_prob(odds2)

    # # print(prob1+prob2)
    # # print(prob1)
    # # input()


print(len(y_true))
print(len(y_open))
print(len(y_close))

y_true = np.array(y_true)
y_open = np.array(y_open)
y_close = np.array(y_close)








# plot_roc_curve(y_true,y_open, savefile="figs/mlb_roc.pdf")


# plot_pr_curve(y_true,y_open, savefile="figs/mlb_pr.pdf")


print_stats(y_true,y_open,round=1)

calibration(y_true,y_open)

# plt.hist(y_open,bins=20)
# plt.show()

