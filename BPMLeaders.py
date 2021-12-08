import os

import pandas as pd

import unidecode

for file in os.listdir("BPM by Year"):
    globals()[file[:-4]] = pd.read_csv('BPM by Year/' + file, dtype=str, header=None)
    globals()[file[:-4]] = globals()[file[:-4]].rename(columns={0: "Name", 1: "Team", 2: "BPM"})
    globals()[file[:-4]]["Name"]= [unidecode.unidecode(x) for x in globals()[file[:-4]]["Name"]]

BPM_globals = globals()