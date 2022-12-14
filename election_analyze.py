import sys
import numpy as np 
import csv
# from sklearn import metrics
# import matplotlib.pyplot as plt

from eval_functions import *


## data source:
#https://electionbettingodds.com/TrackRecord.html




data = []
## read CSV / TSV

y_true = []
y_score = []

with open("data/election_odds.csv") as tsvfile:
    spamreader = csv.reader(tsvfile, delimiter=',')

    next(spamreader)
    for row in spamreader:
        print(row)

        prob = row[2]
        if prob[-1]=="%":
            prob = prob[:-1]

        prob = float(prob)/100
        print(prob)

        y_score.append(prob)

        if row[3]=="Won":
            y_true.append(1)
        elif row[3]=="Lost":
            y_true.append(0)



        # input()


        # data.append([row[0], row[2], row[3], float(row[7]),float(row[8]) ])
        # Date, VH, Team, Final score, ML odds, 
        # input()


assert len(y_true) == len(y_score)

# plot_roc_curve(y_true,y_score, savefile="figs/election_roc.pdf")


# plot_pr_curve(y_true,y_score, savefile="figs/election_pr.pdf")

print_stats(y_true,y_score,round=1)


# plt.hist(y_score,bins=20)
# plt.show()
# entropy(y_score)


calibration_file = "plots/ebo_calibration.jpg"
roc_file = "plots/ebo_roc.jpg"
pr_file = "plots/ebo_pr.jpg"


calibration_plot(y_true,y_score,savefile="plot_pages/"+calibration_file, show=0, title="Calibration - Election Betting Odds")

plot_roc_curve(y_true,y_score,savefile="plot_pages/"+roc_file, show=0, title="ROC - Election Betting Odds")

plot_pr_curve(y_true,y_score,savefile="plot_pages/"+pr_file, show=0, title="PR - Election Betting Odds")

make_html_file("plot_pages/ebo_plots.html", calibration_file=calibration_file, roc_file=roc_file,pr_file=pr_file)
