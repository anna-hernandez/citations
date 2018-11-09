
# import libraries
try:
    from bs4 import BeautifulSoup as bs
    import requests
    import json
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import time
    import math
    import retrieve_pubmed_module as pm
except Exception as e:
    print(e)



# get summary data for publications with myquery in the title between the specified dates
myquery = '\"kaposi-sarcoma' + '\'s associated virus"'
citations_bydate = pd.DataFrame.from_dict(pm.getPubmedsByDate(myquery, 'title', (2001,2002)), orient='index')
citations_bydate.index.name = 'id_citation'

# ------------------------------------- EXAMPLE CASE -------------------------------------
# The following code retrieves uses the two functions to retrieve summary data on all papers published
# between 1009 and 2018, for the different species of human herpesviruses, and plots the trends.

# specify the dates range
mindates = np.arange(1990,2017)
maxdates = np.arange(1991,2018)
dates = list(zip(mindates,maxdates))

# define queries
myqueries = np.array(['"herpes simplex virus 1"+OR+"herpes simplex virus type 1"',
                      '"herpes simplex virus 2"+OR+"herpes simplex virus type 2"',
                      '"varicella zoster virus"',
                      '"human cytomegalovirus"',
                      '"epstein-barr"',
                      '\"kaposi-sarcoma' + '\'s associated virus"'])

# retrieve the summary data and store the number of publications, per year and species in an array
totalpubs = np.empty((0,len(dates)))
for q in myqueries:
    qpubs = np.empty((0,len(dates)))
    print('Searching papers containing {} in title'.format(q), end=' ')
    
    for date in dates:
        print('published in {}'.format(date))
        yearpubs = pd.DataFrame.from_dict(pm.getPubmedsByDate(q, 'title', date), orient='index').shape[0]
        print('{} articles found'.format(yearpubs))
        qpubs = np.append(qpubs, yearpubs)
    totalpubs = np.vstack([totalpubs, qpubs])
    
    
# Plot the publications tendencies
# define labels
labels = np.array(['HSV1','HSV2','VZV','HCMV','EBV','KSHV'])

# set up figure size
plt.figure(1, figsize=(9, 5))

# define x range
x = np.arange(len(dates))

# add a plot to the figure for each query
for q in myqueries:
    idx, = np.where(myqueries == q)
    plt.scatter(x, totalpubs[idx][0], marker='.')
    # add text above each line
    plt.text(x = 0+0.5, y = totalpubs[idx][0][0], s = labels[idx[0]])

# Text below each barplot with a rotation at 90°
ticks = ['-'.join(map(str, i)) for i in list([list(d) for d in dates])]
plt.xticks(x, ticks, rotation=90)

plt.title('Number of publications per year')
plt.xlabel('year')
plt.ylabel('number of publications')

plt.show()

