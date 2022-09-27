import sys
import numpy as np 
import csv
# from sklearn import metrics
import matplotlib.pyplot as plt
from eval_functions import *


## data source:
# https://www.sportsbookreviewsonline.com/scoresoddsarchives/nba/nbaoddsarchives.htm








data = []
## read CSV / TSV
with open("data/nba_2020-21.csv") as tsvfile:
    spamreader = csv.reader(tsvfile, delimiter=',')

    next(spamreader)
    for row in spamreader:
        data.append([row[0], row[2], row[3], float(row[8]),float(row[11]) ])
        # Date, VH, Team, Final score, ML odds, 
        # input()



y_true = []
# did home team win?

y_score = []

for i in range(0,len(data), 2):
    assert(data[i][0] == data[i+1][0])
    assert(data[i][1] != data[i+1][1])
    assert( data[i+1][1]=="H")

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


assert len(y_true) == len(y_score)

plot_roc_curve(y_true,y_score, savefile="figs/nba_roc.pdf")


plot_pr_curve(y_true,y_score, savefile="figs/nba_pr.pdf")


print_stats(y_true,y_score)


