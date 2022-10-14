from eval_functions import *
import random

## coin clip data, predicting 0.5 every time

y_true = []
y_score = []

for i in range(1000):

    y_true.append(random.randint(0,1))
    y_score.append(0.5)
    # y_score.append(1-random.random())



output = ujs(y_true,y_score)

print(output)
