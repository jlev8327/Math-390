import pandas as pd
import numpy as np
import BPMLeaders
import seaborn as sns
import matplotlib.pyplot as plt

data21 = pd.read_csv("odds data/nba odds 2021-22.csv")
data21["Year"] = 2022
data20 = pd.read_csv("odds data/nba odds 2020-21.csv")
data20["Year"] = 2021

abr_dict = {
    'Atlanta': 'ATL',
    'Brooklyn': 'BKN',
    'Boston': 'BOS',
    'Charlotte': 'CHA',
    'Chicago': 'CHI',
    'Cleveland': 'CLE',
    'Dallas': 'DAL',
    'Denver': 'DEN',
    'Detroit': 'DET',
    'GoldenState': 'GSW',
    'Houston': 'HOU',
    'Indiana': 'IND',
    'LAClippers': 'LAC',
    'LALakers': 'LAL',
    'Memphis': 'MEM',
    'Miami': 'MIA',
    'Milwaukee': 'MIL',
    'Minnesota': 'MIN',
    'NewOrleans': 'NOP',
    'NewYork': 'NYK',
    'OklahomaCity': 'OKC',
    'Orlando': 'ORL',
    'Philadelphia': 'PHI',
    'Phoenix': 'PHX',
    'Portland': 'POR',
    'Sacramento': 'SAC',
    'SanAntonio': 'SAS',
    'Toronto': 'TOR',
    'Utah': 'UTA',
    'Washington': 'WAS'}

data21["Open"] = [0 if x in ["pk", "PK"] else x for x in data21["Open"]]
data21["Close"] = [0 if x in ["pk", "PK"] else x for x in data21["Close"]]

data20["Open"] = [0 if x in ["pk", "PK"] else x for x in data20["Open"]]
data20["Close"] = [0 if x in ["pk", "PK"] else x for x in data20["Close"]]

data19["Open"] = [0 if x in ["pk", "PK"] else x for x in data19["Open"]]
data19["Close"] = [0 if x in ["pk", "PK"] else x for x in data19["Close"]]

data18["Open"] = [0 if x in ["pk", "PK"] else x for x in data18["Open"]]
data18["Close"] = [0 if x in ["pk", "PK"] else x for x in data18["Close"]]

data = data20.values.tolist() + data21.values.tolist()

data2 = []

for x in range(0, len(data), 2):
    i1 = float(data[x+1][9])
    i2 = float(data[x][9])
    so = 0
    if(i1<i2):
        so = -i1
    else:
        so = i2
    i3 = float(data[x + 1][10])
    i4 = float(data[x][10])
    sc = 0
    if (i3 < i4):
        sc = -i3
    else:
        sc = i4
    date = str(data[x][0])
    if len(date) == 4:
        date = str(data[x][-1] - 1) + "-" + date[0:2] + "-" + date[2:]
    else:
        date = str(data[x][-1]) + "-" + "0" + date[0] + "-" + date[1:]
    data2 += [[date, data[x][3], data[x+1][3], data[x][8], data[x+1][8], so, sc, data[x][-1]]]

df = pd.DataFrame(data2, columns=['GAME_DATE', 'Away Team', 'Home Team', 'Away Score', 'Home Score', 'Spread Open',
                                  'Spread Close', 'Year'])

df['Home Team'] = df['Home Team'].apply(lambda x: abr_dict[x])
df['Away Team'] = df['Away Team'].apply(lambda x: abr_dict[x])

df["Movement"] = df["Spread Open"] - df["Spread Close"]

df = df[abs(df["Spread Open"]) < 100]
df = df[abs(df["Spread Close"]) < 100]

print(np.std(df["Movement"]))

df["Shift"] = df["Spread Open"] - df["Spread Close"]

df["Shift"] = ["Home" if x > 0 else "Away" for x in df["Shift"]]

df["Covered"] = df["Home Score"] - df["Away Score"] + df["Spread Close"]

df["Covered"] = ["Home" if x > 0 else "Push" if x == "0" else "Away" for x in df["Covered"]]

df = df[df["Covered"] != "Push"]

results = []

for x in range(1, 20, 1):
    df2 = df.copy()
    df2 = df2[abs(df["Movement"]) >= x/2.0]
    results += [[x/2.0, sum(df2["Shift"]==df2["Covered"]), len(df2)]]

results = pd.DataFrame(results, columns=['Cutoff', 'Wins', 'Games'])

results['Success Rate'] = results['Wins']/ results['Games']

print(results)

games_df = pd.read_csv('games.csv', dtype=str)


df = pd.merge(df, games_df[["Away Team", "Home Team", "GAME_ID", "GAME_DATE"]],
              on=["Away Team", "Home Team", "GAME_DATE"])

df = df.drop_duplicates()

out_players = pd.read_csv('all_outs.csv', dtype=str)[["GAME_ID", "Player"]]

df["Player's Out"] = [out_players[out_players["GAME_ID"]==x]["Player"].values for x in df["GAME_ID"]]

df_double1 = df.copy()
df_double1["Team"] = df_double1["Home Team"]

df_double2 = df.copy()
df_double2["Team"] = df_double1["Away Team"]

df_double = pd.concat([df_double1, df_double2]).sort_values('GAME_DATE')

df_double = df_double.reset_index()

df_double['Prev Out'] = df_double.groupby('Team')["Player's Out"].shift(fill_value=set())

df_double["Player's Out"] = df_double["Player's Out"].apply(lambda x: set(x))

df_double['Prev Out'] = df_double['Prev Out'] .apply(lambda x: set(x))

df_double['New Out'] = [list(x[0].difference(x[1])) for x in zip(df_double["Player's Out"], df_double['Prev Out'])]

df = df_double

df["Key Player Out"] = [
    len(set(x[0]).intersection(set(BPMLeaders.BPM_globals
                                   ["BPM_" + str(x[1]-1)]["Name"][:40])))>0 for x in df[["New Out", "Year"]].values]

df = df.drop(["index", "Player's Out", "Prev Out", "New Out", "Team"], axis=1)

print(df)

df = df.groupby(list(df.columns[:-1])).any("Key Player Out").reset_index()

print(len(df))
print(len(df[abs(df["Movement"])>=2]))

results = []

for x in range(1, 20, 1):
    df2 = df[df["Key Player Out"]].copy()
    df2 = df2[abs(df["Movement"]) >= x/2.0]
    results += [[x/2.0, sum(df2["Shift"]==df2["Covered"]), len(df2)]]

results = pd.DataFrame(results, columns=['Cutoff', 'Wins', 'Games'])

results['Success Rate'] = results['Wins']/ results['Games']

print(results)

results = []

for x in range(1, 20, 1):
    df2 = df[df["Key Player Out"] == False].copy()
    df2 = df2[abs(df["Movement"]) >= x/2.0]
    results += [[x/2.0, sum(df2["Shift"]==df2["Covered"]), len(df2)]]

results = pd.DataFrame(results, columns=['Cutoff', 'Wins', 'Games'])

results['Success Rate'] = results['Wins']/ results['Games']

print(results)

df_profits = df[(abs(df["Movement"])>=2) & (df["Key Player Out"])]

df_profits["Profit"] = df["Shift"] == df["Covered"]

df_profits["Profit"] = [100 if x else -110 for x in df_profits["Profit"]]

df_profits = df_profits.groupby("GAME_DATE").sum().sort_values("GAME_DATE")

df_profits = df_profits.assign(sum=df_profits.Profit.cumsum())

print(df_profits)

df_winpct = df[(abs(df["Movement"])>=2) & (df["Key Player Out"])]

df_winpct["Win Pct"] = df["Shift"] == df["Covered"]

df_winpct["Win Pct"] = [1 if x else 0 for x in df_winpct["Win Pct"]]

df_winpct["Games"] = [1 for x in df_winpct["Win Pct"]]

df_winpct = df_winpct.groupby('Year').sum().sort_values('Year')

df_winpct["Win Pct"] = df_winpct["Win Pct"]/ df_winpct["Games"]

df_winpct['Year'] = df_winpct.index

sns.lineplot(x = "GAME_DATE", y = "sum", data = df_profits).set(xticks=["2020-12-27", "2021-03-01",
                                                                        "2021-05-12", "2021-11-30"],
                                                                        xticklabels=["2020-12-27",
                                                                                     "2021-03-01",
                                                                        "2021-05-01", "2021-11-30"])

#sns.catplot(x="Year", y="Win Pct", data=df_winpct, kind="bar")

#plt.axhline(y=0.5328, color='black', linestyle='--')

plt.show()
