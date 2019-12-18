# Development code will go here.

import pandas as pd
from datetime import datetime, timedelta
from sportsreference.ncaab.teams import Teams
from sportsreference.ncaab.schedule import Schedule
from sportsreference.ncaab.boxscore import Boxscore, Boxscores

# Fetch yesterday's boxscores and write to csv.
yesterday = datetime.today() - timedelta(days=1)
boxscores = Boxscores(yesterday)

for date, games in boxscores.games.items():
    game_dataframes = []
    for game in games:
        game_details = Boxscore(game['boxscore'])
        game_dataframes.append(game_details.dataframe)
    full_dataframe = pd.concat(game_dataframes)
    date_string = datetime.strptime(date, '%m-%d-%Y').strftime('%Y-%m-%d')
    file_name = 'boxscores_' + date_string + '.csv'
    full_dataframe.to_csv(file_name, index=False)
