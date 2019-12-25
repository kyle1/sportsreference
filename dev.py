import os
import pandas as pd
import time
from sportsreference.nfl.schedule import Schedule as NflSchedule
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


def get_games_by_week(week):
    game_dataframes = []
    for team_abbrev in TEAM_ABBREVS:
        print('Getting schedule for ' + team_abbrev + '...')
        sched = NflSchedule(team_abbrev)
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


season = '2019'
weeks = ['01', '02', '03', '04', '05', '06', '07', '08',
         '09', '10', '11', '12', '13', '14', '15', '16']

for week in weeks:
    outdir = 'csv/nfl/' + season + '/week' + str(week)
    if not os.path.exists(outdir):
        os.mkdir(outdir)

    games_dataframe = get_games_by_week(int(week))
    games_dataframe.to_csv(outdir + '/games_week_' +
                           str(week) + '.csv', index=False)

    uri_list = games_dataframe['boxscore_index'].tolist()
    uri_list = list(set(uri_list))  # Get unique values
    for uri in uri_list:
        player_boxscores_dataframe = get_boxscores_by_uri(uri)
        player_boxscores_dataframe.to_csv(
            outdir + '/player_boxscores_' + uri + '.csv', index=False)
        time.sleep(5)
