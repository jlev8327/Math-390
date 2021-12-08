from nba_api.stats.endpoints import leaguegamefinder

gamefinder = leaguegamefinder.LeagueGameFinder()

games_df = leaguegamefinder.LeagueGameFinder().get_data_frames()[0]

def changehome(string):
    if "@" in string:
        return string.split(" ")[2]
    return string.split(" ")[0]

def changeaway(string):
    if "@" in string:
        return string.split(" ")[0]
    return string.split(" ")[2]

games_df["Home Team"] = [changehome(x) for x in games_df["MATCHUP"]]
games_df["Away Team"] = [changeaway(x) for x in games_df["MATCHUP"]]

games_df = games_df[games_df["GAME_DATE"]>"2018-10-15"]

teams = ['ATL', 'BKN', 'BOS', 'CHA', 'CHI', 'CLE', 'DAL', 'DEN', 'DET', 'GSW', 'HOU', 'IND', 'LAC', 'LAL', 'MEM',
         'MIA', 'MIL', 'MIN', 'NOP', 'NYK', 'OKC', 'ORL', 'PHI', 'PHX', 'POR', 'SAC', 'SAS', 'TOR', 'UTA', 'WAS']
games_df = games_df[games_df["Home Team"].isin(teams)]

games_df = games_df[["Home Team", "Away Team", "GAME_DATE", "GAME_ID"]]

games_df = games_df.drop_duplicates()

games_df.to_csv("games.csv")