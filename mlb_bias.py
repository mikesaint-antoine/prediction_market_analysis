import sys
import numpy as np 
import csv
# from sklearn import metrics
import matplotlib.pyplot as plt
from eval_functions import *
from sklearn.metrics import r2_score




## data source:
# https://sportsbookreviewsonline.com/scoresoddsarchives/mlb/mlboddsarchives.htm





fb_data = []
## read CSV / TSV
teams = []
fans = []
with open("mlb_only/facebook_likes.csv") as tsvfile:
    spamreader = csv.reader(tsvfile, delimiter=',')

    # next(spamreader)
    for row in spamreader:
        # print(row)
        # input()
        fb_data.append([row[2],float(row[1])])
        teams.append(row[2])
        fans.append(float(row[1]))




print(teams)

print(len(teams))
# sys.exit("trying to read facebook data")









# print(odds_to_prob(190))
# print(odds_to_prob(-210))



# print("test")


# data = []
# ## read CSV / TSV
# with open("mlb_only/mlb_2021.csv") as tsvfile:
#     spamreader = csv.reader(tsvfile, delimiter=',')

#     next(spamreader)
#     for row in spamreader:
#         data.append([row[0],row[2], row[3], float(row[14]), float(row[15]),float(row[16])])
#         # Date, VH, Team, Final score, Odds open, Odds close



# data = []

# with open("mlb_only/mlb_2020.csv") as tsvfile:
#     spamreader = csv.reader(tsvfile, delimiter=',')

#     next(spamreader)
#     for row in spamreader:
#         data.append([row[0],row[2], row[3], float(row[14]), float(row[15]),float(row[16])])
#         # Date, VH, Team, Final score, Odds open, Odds close


data = []
with open("mlb_only/mlb_2017.csv") as tsvfile:
    spamreader = csv.reader(tsvfile, delimiter=',')

    next(spamreader)
    for row in spamreader:
        try:
            data.append([row[0],row[2], row[3], float(row[14]), float(row[15]),float(row[16])])
        except:
            data.append([row[0],row[2], row[3], float(row[14]), 0,0])
        # Date, VH, Team, Final score, Odds open, Odds close




# with open("mlb_only/mlb_2018.csv") as tsvfile:
#     spamreader = csv.reader(tsvfile, delimiter=',')

#     next(spamreader)
#     for row in spamreader:
#         data.append([row[0],row[2], row[3], float(row[14]), float(row[15]),float(row[16])])
#         # Date, VH, Team, Final score, Odds open, Odds close



y_true = []
# did home team win?

y_open = []
y_close = []


new_data = []

for i in range(0,len(data), 2):
    assert(data[i][0] == data[i+1][0])
    assert(data[i][1] != data[i+1][1] or data[i+1][1]=="N")
    # assert( data[i+1][1]=="H")


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




        new_data.append([data[i][2], odds_to_prob(data[i][4]), odds_to_prob(data[i][5]), 0])
        new_data.append([data[i+1][2], odds_to_prob(data[i+1][4]), odds_to_prob(data[i+1][5]), 1])






    else:
        y_true.append(0)
        y_open.append(prob2_open)
        # y_open.append(prob2_open / (prob1_open+prob2_open))

        y_close.append(prob2_close)



        new_data.append([data[i][2], odds_to_prob(data[i][4]), odds_to_prob(data[i][5]), 1])
        new_data.append([data[i+1][2], odds_to_prob(data[i+1][4]), odds_to_prob(data[i+1][5]), 0])






# print("new data...")
# for row in new_data:
#     print(row)
#     input()


team_probs = []
team_results = []
team_ratios = []


for team in teams:
    print(team)


    probs = []
    outcomes = []

    for i in range(len(new_data)):

        if new_data[i][0]==team:
            print("FOUND!")

            try:
                probs.append(float(new_data[i][1]))
                outcomes.append(new_data[i][3])
            except:
                pass

    try:
        team_probs.append(np.mean(probs))
    except:
        print(probs)
        input(np.mean(probs))
    team_results.append(np.mean(outcomes))
    team_ratios.append(np.mean(probs) / np.mean(outcomes))



print(len(team_probs))
print(len(team_results))
print(len(team_ratios))



print(team_ratios)


plt.scatter(fans,team_ratios)



z = np.polyfit(fans, team_ratios, 1)
y_hat = np.poly1d(z)(fans)
plt.plot(fans, y_hat, "r-", lw=1)

text = f"$y={z[0]:0.10f}\;x{z[1]:+0.4f}$\nR^2 = {r2_score(team_ratios,y_hat):0.4f}"
plt.gca().text(0.35, 0.95, text,transform=plt.gca().transAxes,
     fontsize=14, verticalalignment='top')


plt.show()
sys.exit()












