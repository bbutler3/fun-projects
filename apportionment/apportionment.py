import numpy as np
import pandas as pd
#pd.options.display.float_format = '{:.2f}'.format

# There will always be 435 seats in the House (Apportionment Act of 1911).
total_seats = 435

# Set year to use for apportionment (2010-2018). Use 'census' for 2010 census.
year = '2018'

colnames = ['state','census','estimates_base','2010','2011','2012','2013','2014',
            '2015','2016','2017','2018']
pop = pd.read_excel('nst-est2018-01.xlsx',skiprows=3,skipfooter=7,names=colnames)

# Drop regional and other irrelevant population values from the data.
pop = pop.drop([0,1,2,3,4,13])
pop = pop.reset_index(drop=True)

# Remove the stupid leading periods on the state names.
pop.state = pop.state.str.replace('.', '', regex=False)

# Everybody gets a free seat. Adjust remaining seats accordingly.
pop['seats'] = 1
to_assign = total_seats-50

# Calculate multiplier based on value of n. (n = current seats + 1)
def multiplier(n):
    return 1/np.sqrt(n*(n-1))

while to_assign>0:
    pop['priority'] = multiplier(pop['seats']+1)*pop[year]
    max_priority = pop['priority'].max()
    priority_state_idx = pop[['priority']].idxmax().values[0]
    pop.at[priority_state_idx,'seats'] +=1
    to_assign -= 1

if year=='census':
    pop[['state','seats']].to_csv('census2010_apportionment.csv',index=False)
else:
    pop[['state','seats']].to_csv(year+'_apportionment.csv',index=False)