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
        'Tottenham Hotspur': 'Tottenham',
        'West Bromwich Albion': 'West Brom',
        'West Ham United': 'West Ham'
    }.get(team, team)
    
def getOpponent(week, team):
    if(week.Home == team):
        return week.Away + ' (H)'
    else:
        return week.Home + ' (A)'

def getTeamSchedule(all_weeks, team):
    return all_weeks[(all_weeks.Home == team) | (all_weeks.Away == team)] 
      
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
            all_games[count][0] = teams[0].replace('\n', '')
            all_games[count][1] = teams[1].replace('\n', '')
            count += 1



games_df = pd.DataFrame({'Home':all_games[:,0],'Away':all_games[:,1]})
#From: https://stackoverflow.com/questions/27804729/python-groupby-error-unhashable-series-object
games_df_updated = games_df.applymap(str).applymap(switch_team_name)

teams = list(games_df_updated.Home.unique())
teams.sort()

all_schedules = {}
for team in teams: 
    team_schedule = getTeamSchedule(games_df_updated, team)
    opponents = team_schedule.apply(lambda week: getOpponent(week, team), 1)
    all_schedules[team] = np.array(opponents)
    
all_schedules_df = pd.DataFrame.from_dict(all_schedules, orient='index')
all_schedules_df = all_schedules_df.sort_index()
all_schedules_df.columns = ['Week ' + str(i) for i in range(1, 39)]

writer = pd.ExcelWriter('Premier-League_2016-2017_WeekByWeek.xlsx')
row = 0
for i in range (3):
    all_schedules_df.to_excel(writer,sheet_name='Schedule',startrow=row , startcol=0)   
    row = row + len(all_schedules_df.index) + 2
writer.save()

        