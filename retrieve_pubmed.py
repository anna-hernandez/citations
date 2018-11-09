
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
except Exception as e:
    print(e)


# retrieve summary data for a list of pubmed ids using ncbi e-utilities
def getPubmedSummary(pmidlist):

    mainurl = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    esummary = 'esummary.fcgi?db=pubmed&api_key=540abc288c5f8d3ffdb5a9926db491b33a09&retmode=json&id={}'.format(','.join(pmidlist))

    # handle connection error. If the connection is refused, sleep and re-try
    parsed = ''
    while parsed == '':
        try:
            data = requests.get(mainurl+esummary)
            parsed = json.loads(data.text)
            dct = {}
        except requests.exceptions.ConnectionError:
            print("Connection refused. Waiting 5 seconds before trying again.")
            time.sleep(5)
            continue
    
    for pmid in pmidlist:
        dct[pmid] = {}
        authors = []

        dct[pmid]['authors'] = []
        dct[pmid]['pub'] = ' '.join(parsed['result'][pmid]['pubdate'].split()[0:2])
        for a in range(0,len(parsed['result'][pmid]['authors'])):
            authors.append(parsed['result'][pmid]['authors'][a]['name'])
        dct[pmid]['authors'] = ', '.join(authors)
        dct[pmid]['title'] = parsed['result'][pmid]['title']
        dct[pmid]['journal'] = parsed['result'][pmid]['source']
        for i in parsed['result'][pmid]['articleids']:
            if i['idtype'] == 'doi':
                dct[pmid]['doi'] = i['value']
    return dct

# retrieve list of pubmed ids within a specific set of time defined by mindate and maxdate
# call the getPubmedSummary for the returned pmid list
def getPubmedsByDate(query, searchfield, mindate, maxdate):
    
    mainurl = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    esearch = 'esearch.fcgi?db=pubmed&api_key=540abc288c5f8d3ffdb5a9926db491b33a09&term={}&field={}&retmax=100000&datetype=pdat&mindate={}&maxdate={}'.format(theQuery, theSearchfield, theDates[0], theDates[1])
    
    # handle connection error. If the connection is refused, sleep and re-try
    parsed = ''
    while parsed == '':
        try:
            data = requests.get(mainurl + esearch)
            parsed = bs(data.text, 'lxml')
            
        except requests.exceptions.ConnectionError:
            print("Connection refused. Waiting 5 seconds before trying again.")
            time.sleep(5)
            continue
            
    ids = parsed.find_all('id')
    pmidlist = []
    for i in ids:
        pmidlist.append(i.get_text())
        
    summaries = {}
    for alist in [pmidlist[i:i + 300] for i in range(0, len(pmidlist), 300)]:
        summaries.update(getPubmedSummary(alist))
    return summaries

# --------------- main code --------------------

# call getPubmedSummary()
pmids = ['7931156']
citation_dct = getPubmedSummary(pmids)
# format into dataframe and display
citations = pd.DataFrame.from_dict(citation_dct, orient='index')
citations.index.name = 'id_citation'
citations.head()


# call getPubmedsByDate()
myquery = '"herpes simplex virus 1"+OR+"herpes simplex virus type 1"'
# format into dataframe and display
citations_bydate = pd.DataFrame.from_dict(getPubmedsByDate(myquery, 'title',2017,2018), orient='index')
citations_bydate.index.name = 'id_citation'
citations_bydate.head()


# call getPubmedSummary()
# send request for sample pmid list and retrieve pubmed summaries
pmids = ['7931156','8380085','8523566','8661404','8805706','8805708','29035172']
citation_dct = getPubmedSummary(pmids)
# format into dataframe and display
citations = pd.DataFrame.from_dict(citation_dct, orient='index')
citations.index.name = 'id_citation'
citations.head()



