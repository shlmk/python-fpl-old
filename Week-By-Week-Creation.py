# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 20:38:24 2016

@author: MMS
"""

from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd


def switch_team_name(team):
    return{
        'AFC Bournemouth': 'Bournemouth',
        'Hull City': 'Hull',
        'Leicester City': 'Leicester',
        'Manchester City': 'Man City',
        'Manchester United': 'Man United',
        'Stoke City': 'Stoke',
        'Swansea City': 'Swansea', 
        'Tottenham Hotspur': 'Spurs',
        'West Bromwich Albion': 'West Brom',
        'West Ham United': 'West Ham'
    }.get(team, team)
    
    
r = requests.get('http://www.espnfc.us/english-premier-league/story/'+
                     '2890569/premier-league-fixtures-2016-17')
                     
soup = BeautifulSoup(r.text)

paragraphs = soup.find_all('p')
all_games = np.empty((380, 2), dtype=object)
count = 0

for p in paragraphs:
    for games in p.childGenerator():
        str_games = str(games)
        if "vs." not in str_games:
            continue
        else: 
            teams = str_games.split(' vs. ')
            print(teams[0])
            all_games[count][0] = teams[0].replace('\n', '')
            all_games[count][1] = teams[1].replace('\n', '')
            count += 1



games_df = pd.DataFrame({'Home':all_games[:,0],'Away':all_games[:,1]})
games_df_updated = games_df.applymap(str).applymap(switch_team_name)


        