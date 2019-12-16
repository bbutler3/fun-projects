"""
Created 12/15/2019

This script is designed to list all players on current NFL rosters with
a certain letter in their last name (as specified in the "letter"
variable near the top). Michael Cheiken proposed the idea when I asked
him for suggestions of simple-ish sports projects that would teach me
web-scraping.

I used lineups.com partially because it was the first Google result
when I searched "nfl rosters" and partially because it claims to have
live updates. This means we'll (theoretically) get the most up-to-date
rosters at any given time.

Updated 12/15/2019 (lol)

Cheiken wants any string of characters to be recognizable in a name.
For last name alone, this can be done easily by replacing "letter"
with "chars", signifying an expansion of the options for setting the
variable. However, I'd also like to extend to the first name, *and*
allow for crossover to last name. For example, consider the characters
"ff". We would easily find this in "Jefferson". But we'd also like to
identify it in "Sharif Finch". Now we need to eliminate whitespace for
checking, and also check all capitalization permutations.
"""

import time
import pandas as pd

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re


# Generate all capitalization permutations of a set of characters.
def permute_letters(chars):
    permutations = []
    chars = chars.lower()
    n = len(chars)
    x = 1 << n

    for i in range(x):
        combo = [c for c in chars]
        for j in range(n):
            if (((i >> j) & 1) == 1):
                combo[j] = chars[j].upper()

        perm = ''.join(combo)
        permutations.append(perm)

    return permutations


# Specify whether we're searching the last name or the full name.
full = False
# Specify letter to search names for.
chars = 'ff'

# Main page url for the website we're scraping.
stem = 'https://www.lineups.com'

# Specify webpage where the links to NFL rosters live, and download its
# HTML code.  This is then parsed by BeautifulSoup and searched for
# roster links.  Note: the retrieved links aren't full links. See below.
rosters_url = stem + '/nfl/rosters/'
rosters_html = urlopen(rosters_url)
rosters_soup = BeautifulSoup(rosters_html, 'lxml')
nfl_ros = '^/nfl/roster'
link_chunks = rosters_soup.find_all('a', attrs={'href': re.compile(nfl_ros)})

# Construct links to team rosters.  This requires appending the main
# website url to the beginning of each.
team_links = []
i = 0
for chunk in link_chunks:
    # Each link on the page is duplicated for some reason.  This is
    # remedied here.  Also, the first two links in the list are not team
    # links, so they are removed.
    if (i % 2) == 0 and i > 1:
        link = chunk.get('href')
        team_links.append(link)
    i += 1

# A list of suffixes for later removal from the last name.
# This saves (e.g.) "Butler III" from being identified as containing i.
suffixes = ['Jr', 'Sr', 'II', 'III', 'IV', 'V']

for link in team_links:
    matches = []
    ct = 0

    # Construct individual roster url and retrieve roster with Pandas.
    team_url = stem + link
    roster = pd.read_html(team_url)[0]

    # Loop through each player and engineer their name from the mess
    # returned in the dataframe.  Example 'Name' column entry for
    # Leighton Vander Esch:
    # 'Leighton Vander Esch  L. V. Esch'
    for name_chunk in roster['Name']:
        # Luckily, there are two spaces before the abbreviated name,
        # so we can split on a double space to retrieve the full name.
        full_name = name_chunk.split('  ')[0]
        name_list = full_name.split(' ')
        if full:
            for suffix in suffixes:
                if suffix in name_list:
                    name_list.remove(suffix)
            name_nospace = ''.join(name_list)
            for perm in permute_letters(chars):
                if perm in name_nospace:
                    matches.append(full_name)
                    ct += 1
                    break
        else:
            # Make last name into list (in case it contains > 1 word).
            last_list = name_list[1:]

            # Remove suffix from last name.
            for suffix in suffixes:
                if suffix in last_list:
                    last_list.remove(suffix)
            last = ' '.join(last_list)
            if (chars in last) or (chars.title()) in last:
                matches.append(full_name)
                ct += 1

    # If a player with matching name is on the roster, print team name.
    # (optionally with its rank 1-32 in alphabetical order by city).
    # Then print matching players.
    if ct > 0:
        team_hyphen = link.split('/')[-1]
        team_name = team_hyphen.replace('-', ' ').title()
        team_print = team_name
        spacing = ' '*2
        print(team_print)

        for m in matches:
            print(spacing + m)

        print()

    time.sleep(1)
