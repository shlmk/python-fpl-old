# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 18:05:04 2016

@author: MMS
"""

from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import PatternFill
from openpyxl import load_workbook
import ast
from functools import reduce

#TODO: Make better placement of this
teams = ['Arsenal','Bournemouth','Burnley',
         'Chelsea', 'Crystal Palace', 'Everton',
         'Hull','Leicester','Liverpool','Man City',
         'Man United','Middlesbrough','Southampton',
         'Spurs','Stoke','Sunderland','Swansea',
         'Watford','West Brom','West Ham']
       
def process_week(week_html):
    week = week_html.text
    
    #From: https://stackoverflow.com/questions/6116978/python-replace-multiple-strings
    repls = ('true','True'), ('false', 'False'), ('null', '[]')
    week = reduce(lambda a, kv: a.replace(*kv), repls, week)
    week = ast.literal_eval(week)
            
#NOTE: weeks must be a list format
def record_data(weeks):
    url = 'https://fantasy.premierleague.com/drf/fixtures/?event='

    if type(weeks) is not list:
        raise TypeError('Weeks must be of type list')
    else:
        for week_num in weeks:
            if type(week_num) is not int:
                raise TypeError('Week must be an int value')
            elif week_num < 1 or week_num > 38:
                raise IndexError('Week must be between 1 and 38')
            else: 
                url += str(week_num)
        
            print(url)
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            
            process_week(soup)


          