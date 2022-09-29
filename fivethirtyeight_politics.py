import sys
import numpy as np 
import csv
# from sklearn import metrics
import matplotlib.pyplot as plt
from eval_functions import *

## data source:
# https://github.com/fivethirtyeight/checking-our-work-data



# topic = "house"
# topic = "governors"
topic = "senate"



# seasons = [""]

data = []
## read CSV / TSV

y_true = []
y_score = []


with open(f"data/fivethirtyeight_{topic}.csv") as tsvfile:
    spamreader = csv.reader(tsvfile, delimiter=',')

    next(spamreader)
    for row in spamreader:
        # print(row)

        # input()

        if topic in ["house","senate"]:

            y_true.append(int(row[12]))
            y_score.append(float(row[11]))
 

        elif topic in ["governors"]:

            y_true.append(int(row[13]))
            y_score.append(float(row[12]))


assert len(y_true) == len(y_score)

plot_roc_curve(y_true,y_score, savefile=f"figs/fte_{topic}_roc.pdf")


plot_pr_curve(y_true,y_score, savefile=f"figs/fte_{topic}_pr.pdf")

print_stats(y_true,y_score)