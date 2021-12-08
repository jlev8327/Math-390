import pandas as pd
import numpy as np
import nba_api.stats.endpoints

games = pd.read_csv('games.csv', dtype=str)
games = games[games["GAME_DATE"]>"2018-10-15"]
games = games[games["GAME_DATE"]<"2019-10-21"]

def player_out(gameid):
    return [" ".join(x[1:3]) for x in nba_api.stats.endpoints.BoxScoreSummaryV2(gameid).inactive_players.data['data']]

outs = []

#1597 total games

for x in games["GAME_ID"][1500:]:
    players = player_out(x)
    outs += [[x, y] for y in players]

outs = pd.DataFrame(outs, columns=['GAME_ID', 'Player'])

outs.to_csv("player_out42.csv")