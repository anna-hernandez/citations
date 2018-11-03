
# coding: utf-8

# In[166]:


try:
    from bs4 import BeautifulSoup as bs
    import requests
    import json
    import numpy as np
    import pandas as pd
except Exception as e:
    print(e)


# In[ ]:


def getPubmedSummary(pmidlist):

    mainurl = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/'
    esummary = 'esummary.fcgi?db=pubmed&retmode=json&id={}'.format(','.join(pmidlist))
    esearch = 'esearch.fcgi?db=pubmed&term=asthma&field=title'
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


# In[215]:


# send request and retrieve pubmed summaries
pmids = ['7931156','8380085','8523566','8661404','8805706','8805708','8995681','9096314','9159483','9188587','9261356','9336833','9369473','9454723','9715911','9731777','9989588','10233976','10727407','10727769','10797014','10882068','10924157','11041844','11056041','11069986','11086131','11266595','11371196','11511370','11524687','11602734','11739701','11773378','12076828','12093920','12421561','12477844','12549906','12634364','12686543','12743292','12771417','14527394','14557627','15140983','15163659','15286084','15596820','15837194','16014918','16339411','16371349','16483937','16646632','16647084','16731912','16840698','17035316','17446270','17609285','17620619','17855514','17868947','17870089','17913813','18321973','18434401','18682223','18945775','19196955','19370696','19730696','19759157','19801550','20102225','20133758','20205919','20601960','20805464','20943984','21149717','21483780','21623543','21723875','21821792','22028648','22438555','22902366','23500487','23555243','23850455','23938468','24598754','24760889','25678705','25918416','26062451','26085142','26432641','26484870','26511020','26511021','27035968','28663444','29035172']
citation_dct = getPubmedSummary(pmids)

# format into dataframe and display
citations = pd.DataFrame.from_dict(citation_dct, orient='index')
citations.index.name = 'id_citation'
citations.head()



