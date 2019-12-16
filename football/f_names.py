"""
12/15/2019

This script is designed to list all players on current NFL rosters with a certain
letter in their last name (as specified in the "letter" variable near the top).
Michael Cheiken proposed the idea when I asked him for suggestions of simple-ish
sports projects that would teach me web-scraping.

I used lineups.com partially because it was the first Google result when I 
searched "nfl rosters" and partially because it claims to have live updates.
This means we'll (theoretically) get the most up-to-date rosters at any given time.
"""

import time
import pandas as pd

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

# Specify letter to search last names for.
letter = 'f'

# Main page url for the website we're scraping.
stem = 'https://www.lineups.com'

# Specify webpage where the links to NFL rosters live, and download its HTML code.
# This is then parsed by BeautifulSoup and searched for roster links.
# Note: the retrieved links are not full links. More below.
rosters_url = stem + '/nfl/rosters/'
rosters_html = urlopen(rosters_url)
rosters_soup = BeautifulSoup(rosters_html,'lxml')
link_chunks = rosters_soup.find_all('a', attrs={'href':re.compile('^/nfl/roster')})

# Construct links to team rosters. This requires appending the main website url
# to the beginning of each. 
team_links = []
i = 0
for chunk in link_chunks:
    # Each link on the page is duplicated for some reason. This is remedied here.
    # Also, the first two links in the list are not team links, so they are removed.
    if (i % 2) == 0 and i > 1:
        link = chunk.get('href')
        team_links.append(link)
    i+=1

# A list of suffixes for later removal from the last name.
# This saves "Butler III" 
suffixes = ['Jr', 'II', 'III', 'IV', 'V']

for link in team_links:
    idx = team_links.index(link)
    team_hyphen = link.split('/')[-1]
    team_name = team_hyphen.replace('-',' ').title()
    #print('%d. %s' % (idx+1, team_name))
    print(team_name)
    team_url = stem + link
    roster = pd.read_html(team_url)[0]
    for name in roster['Name']:
        name_chunk = name.split('.')[0]
        first_last = name_chunk.split('  ')[0]
        name_list = first_last.split(' ')
        full_name = ' '.join(name_list)
        last_list = name_list[1:]
        for suffix in suffixes:
            if suffix in last_list:
                last_list.remove(suffix)
                if suffix=='Jr':
                    full_name += '.'
        last = ' '.join(last_list)
        if (letter in last) or (letter.upper()) in last: 
            print('  ' + full_name)
    print()
    time.sleep(1)
    