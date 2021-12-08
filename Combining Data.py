import os

import pandas as pd

all_outs = pd.read_csv('player_outs/' + os.listdir("player_outs")[0], dtype=str)

for file in os.listdir("player_outs")[1:]:
    all_outs = pd.concat([all_outs,  pd.read_csv('player_outs/' + file, dtype=str)])

all_outs.to_csv("all_outs.csv")