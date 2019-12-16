import os
if os.path.isfile('./matplotlibrc'):
    from shutil import copyfile
    homerc = os.path.expanduser('~/.matplotlib/matplotlibrc')
    copyfile('./matplotlibrc',homerc)

import numpy as np
import pandas as pd

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = "https://www.pro-football-reference.com/years/NFL/scoring.htm"
"""
html = urlopen(url)

soup = BeautifulSoup(html,'lxml')

table = soup.find_all('table')[2]

rows = table.find_all('tr')

for row in rows:
    row_td = row.find_all('td')
    str_cells = str(row_td)
    cleantext = BeautifulSoup(str_cells,'lxml').get_text()
    print(cleantext)
"""    

df = pd.read_html(url)[2]
df = df.drop([29,60,91])
cols = []
for c in df.columns:
    cols.append(c[1])
    
df.columns = cols

typedict = {}

for c in df.columns:
    if (df[c].isnull().values.any()) or (c=='Pts/G'):
        typedict[c] = 'float'
    else:
        typedict[c] = 'int'
        
df = df.astype(typedict)