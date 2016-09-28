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
    
def extract_ratings(fixtures, team_num):
    diffculty = []
    for fix in fixtures: 
        if(fix['team_h'] == team_num):
            diffculty.append(fix['team_h_difficulty'])
        elif(fix['team_a'] == team_num):
            diffculty.append(fix['team_a_difficulty'])
    return diffculty
    