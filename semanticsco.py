from __future__ import unicode_literals, print_function, absolute_import
from builtins import str
import requests
import re
import json
from doibib import *
from dbcon import Dbcon
import load_dataset

#important topics
# MATCH ()-[r]->(n:Topic) WITH n,count(r) as rel_cnt WHERE rel_cnt > 5 RETURN n, rel_cnt ORDER BY rel_cnt desc;


dbcon = Dbcon('bolt://localhost:7687', 'neo4j', 'password')

# List Decoding for Binary Goppa Code
paperID = "a460c6918ad608a7979b861a04cc42810d449d8e"

# 1975. Nicholas J. Patterson. "The algebraic decoding of Goppa codes."
paperID2 = "c06d89f81c68209ba42430c894354561918b9ffd"

# Coding-Based Oblivious Transfer
paperID3 = "ae6501f58c32817f11b7598c0547714fba6d8a72"


paperID4 = "9ce5eaab06878f434c2efa55959a1212f382ec57"

l = []


def rec(id, i, l, dbcon):
    #l.append(id)
    i -= 1
    r = requests.get("http://api.semanticscholar.org/v1/paper/"+str(id))
    if r.status_code == 200:
        jso = json.loads(r.text)

        doi = jso['doi']
        title = jso['title']
        year = jso['year']
        citations = jso['citations']
        references = jso['references']
        authors = jso['authors']
        topics = jso['topics']

        isDOI = True
        if doi is None:
            doi = "None"
            doi = title
            isDOI = False

        dbcon.create_publi(title, doi, str(year))
        if len(authors) > 0:
            for j in authors:
                createAuth(j, dbcon)
                dbcon.link_auth_publi(j['name'], doi, isDOI=isDOI)

        for j in topics:
            dbcon.create_topic(j['topic'])
            dbcon.link_top_publi(j['topic'], doi, isDOI=isDOI)
        if i > 0:
            for j in citations:
                newID = j['paperId']
                if newID in l:
                    continue
                else:
                    l = rec(newID, i, l, dbcon)
                    if j['doi'] is not None:
                        dbcon.link_ref(
                            j['doi'], doi, isDOI1=True, isDOI2=isDOI)
                    else:
                        dbcon.link_ref(j['title'], doi,
                                       isDOI1=False, isDOI2=isDOI)

            for j in references:
                newID = j['paperId']
                if newID in l:
                    continue
                else:
                    l = rec(newID, i, l, dbcon)
                    if j['doi'] is not None:
                        dbcon.link_ref(
                           doi, j['doi'], isDOI1=isDOI, isDOI2=True)
                    else:
                        dbcon.link_ref(doi, j['title'],
                                       isDOI1=isDOI, isDOI2=False)
    return l


def createAuth(auth, dbcon):

    dbcon.create_author(auth['name'])
    id = auth['authorId']
    if id is not None:
        r = requests.get("http://api.semanticscholar.org/v1/author/"+str(id))
        jso = json.loads(r.text)

        for i in jso['aliases']:
            dbcon.create_author(i)
            dbcon.link_aliases(jso['name'], i)

print("get data")
DOIS,TITLES = load_dataset.get_data()
#for i in DOIS:
#   rec(i, 2, l, dbcon)

body={
    "queryString": "A public-key cryptosystem based on algebraic coding theory",
    "page": 1,
    "pageSize": 1,
    "sort": "relevance",
    "authors": [],
    "coAuthors": [],
    "venues": [],
    "yearFilter": None,
    "requireViewablePdf": False,
    "publicationTypes": [],
    "externalContentTypes": []
}

print('query data')
for i in TITLES:
    r = requests.post("https://www.semanticscholar.org/api/1/search", json=body)
    jso=json.loads(r.text)
    rec(jso['results'][0]['id'], 2, l, dbcon)

# print("pp1")
# l = rec(paperID, 4, l, dbcon)
# print(len(l))
# print("pp2")
# l = rec(paperID2, 4, l, dbcon)
# print(len(l))
# print("pp3")
# l = rec(paperID3, 4, l, dbcon)
# print(len(l))
# print("pp4")
# l = rec(paperID4, 4, l, dbcon)
# print(len(l))

dbcon.close()
