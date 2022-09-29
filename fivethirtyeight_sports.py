import sys
import numpy as np 
import csv
# from sklearn import metrics
import matplotlib.pyplot as plt
from eval_functions import *

## data source:
# https://github.com/fivethirtyeight/checking-our-work-data


# topic = "nba"
# topic = "mlb"
topic = "nfl"



# seasons = [""]

data = []
## read CSV / TSV

y_true = []
y_score = []


with open(f"data/fivethirtyeight_{topic}.csv") as tsvfile:
    spamreader = csv.reader(tsvfile, delimiter=',')

    next(spamreader)
    for row in spamreader:
        print(row)

        # input()

        if topic in ["nba","nfl"]:
            if float(row[5]) in [0,1]:
                # ignore ties, which are labeled 0.5
                y_true.append(int(row[5]))
                y_score.append(float(row[4]))

        elif topic in ["mlb"]:
            if float(row[6]) in [0,1]:
                y_true.append(int(row[6]))
                y_score.append(float(row[5]))     



assert len(y_true) == len(y_score)

plot_roc_curve(y_true,y_score, savefile=f"figs/fte_{topic}_roc.pdf")


plot_pr_curve(y_true,y_score, savefile=f"figs/fte_{topic}_pr.pdf")

print_stats(y_true,y_score)