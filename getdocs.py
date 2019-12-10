# -*- coding: utf-8 -*-
"""getDocs.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1MPI6cF-W1hcf9vMD8QAr0RrBvibaBy6K
"""
from __future__ import unicode_literals, print_function, absolute_import
from builtins import str
import requests
import re
import json
from doibib import get_bib_from_doi

r = requests.get('https://ieeexplore.ieee.org/document/1055350')
text=r.text

#urls= re.findall(r'https:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)',text)
#dois="<a _ngcontent-c35= class=stats-citations-link-crossRef href=https://doi.org/10.1515/JMC.2007.009> CrossRef</a>"
#urls=re.findall(r'https:\/\/doi.org\/\b(10[.][0-9]{4,}(?:[.][0-9]+)*/\S+)',text)
urls=re.findall(r'\b(10[.][0-9]{4,}\S+\.[0-9]+)',text)
print(urls[0])

headers1= {"Referer": "https://ieeexplore.ieee.org/"}
#r=requests.get("https://ieeexplore.ieee.org/rest/document/490862/similar",headers=headers1)
#jso=json.loads(r.text)
#print(jso)
l=[]
Titles=[]
def rec(id, i,l, ):
  global Titles
  l.append(id)
  i-=1
  r=requests.get("https://ieeexplore.ieee.org/rest/document/"+str(id)+"/similar",headers=headers1)
  jso=json.loads(r.text)
  title=jso['formulaStrippedArticleTitle']
  Titles.append(title)
  print(str(i) + " " +title)
  if i>0:
    for j in range(len(jso['similar'])):
      newID=jso['similar'][j]['articleNumber']
      if newID in l :
        return l
      else:
        l=rec(newID,i,l)
  return l

l=rec(1055350,4,l)

print(get_bib_from_doi(urls[0])[1])
