# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 20:40:21 2016

@author: MMS
"""

from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
import ast
from openpyxl import load_workbook

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
    
def extract_ratings(fixtures, team_num):
    print(len(fixtures))
    diffculty = []
    count = 0
    for fix in fixtures: 
        if(fix['team_h'] == team_num):
            diffculty.append(fix['team_h_difficulty'])
            print("YAS")
            count += 1
            print(count)
        elif(fix['team_a'] == team_num):
            diffculty.append(fix['team_a_difficulty'])
            print("YAS2")
            count += 1
            print(count)
    return diffculty
    
r = requests.get('https://fantasy.premierleague.com/drf/fixtures/')
                     
soup = BeautifulSoup(r.text)

paragraph = soup.find("p")

str_fix_list = paragraph.contents

#Do some cleaning
fix_str = str_fix_list[0][1:-1]
fix_str = fix_str.replace(',{\"id\":','SPLIT{\"id\":')

fixture_list = fix_str.split('SPLIT')

fixture_list_corr = []

for idx, fix in enumerate(fixture_list):
    #Clean up the strings and convert them to
    #dicts to make it easier to search
    fix = fix.replace("true","True")
    fix = fix.replace("false", "False")
    fix = fix.replace("null", '[]')
    fixture_list_corr.append(ast.literal_eval(fix))
    
diff_by_team = {}    
for team_num in range(1, 21):
    diff = extract_ratings(fixture_list_corr,team_num)
    diff_by_team[team_num] = np.array(diff)
    
all_schedules_df = pd.DataFrame.from_dict(diff_by_team, orient='index')
all_schedules_df.columns = ['Week ' + str(i) for i in range(1, 39)]
r = requests.get('https://fantasy.premierleague.com/a/team/my')
soup = BeautifulSoup(r.text)

teams_html = soup.findAll("span", { "class" : "name" })

teams = []

for team in teams_html:
    teams.append(team.contents[0])
teams.sort()

teams = list(map(switch_team_name, teams))
all_schedules_df.index = teams

writer = pd.ExcelWriter('Premier-League_2016-2017_WeekByWeek.xlsx')
row = 0
for i in range (3):
    all_schedules_df.to_excel(writer,sheet_name='Difficulty',startrow=row , startcol=0)   
    row = row + len(all_schedules_df.index) + 2
writer.save()
