import sys
import numpy as np 
import csv
# from sklearn import metrics
import matplotlib.pyplot as plt
from eval_functions import *

## data source:
# https://astralcodexten.substack.com/p/grading-my-2021-predictions



year = 2014




data = []
## read CSV / TSV

y_true = []
y_score = []


with open(f"data/ssc_forecasts/ssc_{year}.csv") as tsvfile:
    spamreader = csv.reader(tsvfile, delimiter=',')

    next(spamreader)
    for row in spamreader:
        # print(row)

        # input()

        if row[2] in ["0","1"]:
            # exclude unresolved questions, labeled "NA"
            y_true.append(int(row[2]))
            y_score.append(float(row[1]))
        else:
            print(row[2])







# sys.exit("check read in")


assert len(y_true) == len(y_score)

# plot_roc_curve(y_true,y_score, savefile=f"figs/fte_{topic}_roc.pdf")


# plot_pr_curve(y_true,y_score, savefile=f"figs/fte_{topic}_pr.pdf")

print_stats(y_true,y_score,round=1)