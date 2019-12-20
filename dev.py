# Development code will go here.
import pandas as pd
from datetime import datetime, timedelta
from sportsreference.nba.boxscore import Boxscore as NbaBoxscore
from sportsreference.nba.schedule import Schedule as NbaSchedule
from sportsreference.ncaab.teams import Teams as NcaaTeams
from sportsreference.ncaab.schedule import Schedule as NcaaSchedule
from sportsreference.ncaab.boxscore import Boxscore as NcaaBoxscore, Boxscores as NcaaBoxscores

####################### NCAA #######################
# Fetch yesterday's boxscores and write to csv.
yesterday = datetime.today() - timedelta(days=1)
boxscores = NcaaBoxscores(yesterday)  # Not as detailed as invidiual boxscore

for date, games in boxscores.games.items():
    game_dataframes = []
    for game in games:
        game_details = NcaaBoxscore(game['boxscore'])
        game_dataframes.append(game_details.dataframe)
    full_dataframe = pd.concat(game_dataframes)
    date_string = datetime.strptime(date, '%m-%d-%Y').strftime('%Y-%m-%d')
    file_name = 'boxscores_' + date_string + '.csv'
    full_dataframe.to_csv(file_name, index=False)


####################### NBA #######################
# todo- look into using Boxscores

# NBA_TEAM_ABBREVS = [
#     'MIL', 'BOS', 'MIA', 'TOR', 'PHI', 'IND', 'BRK', 'ORL',
#     'CHO', 'DET', 'CHI', 'WAS', 'NYK', 'CLE', 'ATL', 'LAL',
#     'LAC', 'DEN', 'DAL', 'HOU', 'UTA', 'OKC', 'SAC', 'POR',
#     'PHO', 'MIN', 'SAS', 'MEM', 'NOP', 'GSW'
# ]


# def get_nba_games_by_date(date):
#     game_dataframes = []
#     for team_abbrev in NBA_TEAM_ABBREVS:
#         sched = NbaSchedule(team_abbrev)
#         sched.dataframe['datetime'] = sched.dataframe['datetime'].apply(
#             lambda x: x.date())
#         matches_date = sched.dataframe['datetime'] == pd.Timestamp(date)
#         date_game = sched.dataframe[matches_date]
#         game_dataframes.append(date_game)
#     # Combine the list of dataframes into one.
#     games_dataframe = pd.concat(game_dataframes)
#     return games_dataframe


# date = datetime.today().date() - timedelta(1)  # Yesterday
# date_str = datetime.strftime(date, '%Y-%m-%d')
# games_dataframe = get_nba_games_by_date(date)
# games_dataframe.to_csv('games_' + date_str + '.csv', index=False)

# game_boxscore_dataframes = []
# player_boxscores_dataframes = []
# uri_list = games_dataframe['boxscore_index'].tolist()
# for uri in uri_list:
#     game_boxscore = NbaBoxscore(uri)
#     game_boxscore_dataframes.append(game_boxscore.dataframe)
#     for away_player in game_boxscore.away_players:
#         player_boxscores_dataframes.append(away_player.dataframe)
#     for home_player in game_boxscore.home_players:
#         player_boxscores_dataframes.append(home_player.dataframe)

# # Combine the list of dataframes into one.
# game_boxscores_dataframe = pd.concat(game_boxscore_dataframes)
# game_boxscores_dataframe.to_csv(f'game_boxscores_{date_str}.csv')

# player_boxscores_dataframe = pd.concat(player_boxscores_dataframes)
# player_boxscores_dataframe.to_csv(
#     f'player_boxscores_{date_str}.csv', index=False)
