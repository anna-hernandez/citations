
# import libraries
try:
    from bs4 import BeautifulSoup as bs
    import requests
    import json
    import numpy as np
    import pandas as pd
except Exception as e:
    print(e)


# retrieve summary data for a list of pubmed ids using ncbi e-utilities
def getPubmedSummary(pmidlist):

    mainurl = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    esummary = 'esummary.fcgi?db=pubmed&retmode=json&id={}'.format(','.join(pmidlist))
    data = requests.get(url)
    parsed = json.loads(data.text)
    
    dct = {}
    
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

# --------------- main code --------------------

# send request for sample pmid list and retrieve pubmed summaries
pmids = ['7931156','8380085','8523566','8661404','8805706','8805708','29035172']
citation_dct = getPubmedSummary(pmids)

# format into dataframe and display
citations = pd.DataFrame.from_dict(citation_dct, orient='index')
citations.index.name = 'id_citation'
citations.head()



