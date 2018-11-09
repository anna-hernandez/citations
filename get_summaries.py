
# coding: utf-8

# In[1]:


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


# In[2]:


# send request and retrieve pubmed summaries
pmids = ['7931156']
citation_dct = pm.getPubmedSummary(pmids)

# format into dataframe and display
citations = pd.DataFrame.from_dict(citation_dct, orient='index')
citations.index.name = 'id_citation'
citations.head()


# In[3]:


# format into dataframe and display
myquery = '\"kaposi-sarcoma' + '\'s associated virus"'
citations_bydate = pd.DataFrame.from_dict(pm.getPubmedsByDate(myquery, 'title', (2001,2002)), orient='index')
citations_bydate.index.name = 'id_citation'


# In[4]:


mindates = np.arange(1990,2017)
maxdates = np.arange(1991,2018)
dates = list(zip(mindates,maxdates))


# In[6]:


totalpubs = np.empty((0,len(dates)))
myqueries = np.array(['"herpes simplex virus 1"+OR+"herpes simplex virus type 1"',
                      '"herpes simplex virus 2"+OR+"herpes simplex virus type 2"',
                      '"varicella zoster virus"',
                      '"human cytomegalovirus"',
                      '"epstein-barr"',
                      '\"kaposi-sarcoma' + '\'s associated virus"'])

for q in myqueries:
    qpubs = np.empty((0,len(dates)))
    print('Searching papers containing {} in title'.format(q), end=' ')
    
    for date in dates:
        print('published in {}'.format(date))
        yearpubs = pd.DataFrame.from_dict(pm.getPubmedsByDate(q, 'title', date), orient='index').shape[0]
        print('{} articles found'.format(yearpubs))
        qpubs = np.append(qpubs, yearpubs)
    totalpubs = np.vstack([totalpubs, qpubs])
    


# In[15]:


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

