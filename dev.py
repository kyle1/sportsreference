import os
import pandas as pd
import time
from sportsreference.nfl.schedule import Schedule as NflSchedule
from sportsreference.nfl.roster import Player as NflPlayer
from sportsreference.nfl.roster import Roster as NflRoster
from sportsreference.nfl.boxscore import Boxscore as NflBoxscore, Boxscores as NflBoxscores

TEAM_ABBREVS = [
    'NWE', 'BUF', 'NYJ', 'MIA',
    'RAV', 'PIT', 'CLE', 'CIN',
    'HTX', 'OTI', 'CLT', 'JAX',
    'KAN', 'RAI', 'SDG', 'DEN',
    'PHI', 'DAL', 'WAS', 'NYG',
    'GNB', 'MIN', 'CHI', 'DET',
    'NOR', 'TAM', 'ATL', 'CAR',
    'SFO', 'SEA', 'RAM', 'CRD'
]


uri_list = []
game_df_list = []


def get_games_by_season_and_week(season, week):
    game_dataframes = []
    for team_abbrev in TEAM_ABBREVS:
        print('Getting season ' + str(season) + ', week ' +
              str(week) + ' schedule for ' + team_abbrev + '...')
        sched = NflSchedule(team_abbrev, season)
        matches_week = sched.dataframe['week'] == week
        week_game = sched.dataframe[matches_week]
        game_dataframes.append(week_game)
        time.sleep(5)
    # Combine the list of dataframes into one.
    games_dataframe = pd.concat(game_dataframes)
    return games_dataframe


def get_boxscores_by_uri(uri):
    print('Getting boxscores from ' + uri + '...')
    box = NflBoxscore(uri)
    player_boxscores_dataframes = []
    for away_player in box.away_players:
        player_boxscores_dataframes.append(away_player.dataframe)
    for home_player in box.home_players:
        player_boxscores_dataframes.append(home_player.dataframe)
    # Combine the list of dataframes into one.
    player_boxscores_dataframe = pd.concat(player_boxscores_dataframes)
    return player_boxscores_dataframe


# seasons = ['2018', '2019']
# weeks = ['01', '02', '03', '04', '05', '06', '07', '08',
#          '09', '10', '11', '12', '13', '14', '15', '16']

# for season in seasons:
#     season_path = 'csv/nfl/' + season
#     if not os.path.exists(season_path):
#         os.mkdir(season_path)
#     for week in weeks:
#         week_path = season_path + '/week' + week
#         if not os.path.exists(week_path):
#             os.mkdir(week_path)

#         games_dataframe = get_games_by_season_and_week(int(season), int(week))
#         games_dataframe.to_csv(week_path + '/week' +
#                                week + '_games.csv', index=False)

#         uri_list = games_dataframe['boxscore_index'].tolist()
#         uri_list = list(set(uri_list))  # Get unique values
#         for uri in uri_list:
#             player_boxscores_dataframe = get_boxscores_by_uri(uri)
#             player_boxscores_dataframe.to_csv(
#                 week_path + '/week' + week + '_player_boxscores_' + uri + '.csv', index=False)
#             time.sleep(5)


TEAM_ABBREVS = [
    'NWE', 'BUF', 'NYJ', 'MIA',
]

player_ids = []
for team in TEAM_ABBREVS:
    roster = NflRoster(team, slim=True)
    print(roster._players)
    for k, v in roster._players.items():
        player_ids.append(k)

player_dfs = []
for player_id in player_ids:
    player = NflPlayer(player_id)
    player_dfs.append(player.dataframe)

players_df = pd.concat(player_dfs)
players_df.to_csv('players.csv', index=False)
