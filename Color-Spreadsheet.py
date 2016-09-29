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

#TODO: Make better placement of this
teams = ['Arsenal','Bournemouth','Burnley',
         'Chelsea', 'Crystal Palace', 'Everton',
         'Hull','Leicester','Liverpool','Man City',
         'Man United','Middlesbrough','Southampton',
         'Spurs','Stoke','Sunderland','Swansea',
         'Watford','West Brom','West Ham']
         
#NOTE: weeks must be a list format
def record_data(weeks):
    if type(weeks) is not list:
        raise TypeError('Weeks must be of type list')
    else:
        for week in weeks:
            if type(week) is not int:
                raise TypeError('Week must be an int value')
            elif week < 1 or week > 38:
                raise IndexError('Week must be between 1 and 38')
            else:
                process_week(week)
                
def process_week(week):
    
        
def process_row(row):
    print("DOES NOTHING!")


r = requests.get('http://www.livefootball.co.uk/premier-league/2016-2017/regular-season/gameweek-01/')
soup = BeautifulSoup(r.text)

rows = soup.find_all('tr')
for row in rows:
    if row.has_attr('data-match-id'):
      print("yikes!")
      for game in row.childGenerator():
          print(game)
          