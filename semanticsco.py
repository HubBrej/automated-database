from __future__ import unicode_literals, print_function, absolute_import
from builtins import str
import requests
import re
import json
from doibib import *
from dbcon import Dbcon
import load_dataset


dbcon = Dbcon('bolt://localhost:7687', 'neo4j', 'password')

paperID = "a460c6918ad608a7979b861a04cc42810d449d8e"
# 1975. Nicholas J. Patterson. "The algebraic decoding of Goppa codes."
paperID2 = "c06d89f81c68209ba42430c894354561918b9ffd"

l = []


def rec(id, i, l, dbcon):
    l.append(id)
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

        if doi is None:
            doi = "None"

        dbcon.create_publi(title, doi, year)
        if len(authors) > 0:
            for j in authors:
                createAuth(j, dbcon)
                dbcon.link_auth_publi(j['name'], doi, isDOI=True)

        for j in topics:
            dbcon.create_topic(j['topic'])
            dbcon.link_top_publi(j['topic'], doi, isDOI=True)
        if i > 0:
            for j in citations:
                newID = j['paperId']
                if newID in l:
                    return l
                else:
                    l = rec(newID, i, l, dbcon)
                    if j['doi'] is not None:
                        dbcon.link_ref(j['doi'], doi, isDOI1=True, isDOI2=True)
                    else:
                        dbcon.link_ref(j['title'], doi,
                                       isDOI1=False, isDOI2=True)

            for j in references:
                newID = j['paperId']
                if newID in l:
                    return l
                else:
                    l = rec(newID, i, l, dbcon)
                    if j['doi'] is not None:
                        dbcon.link_ref(
                            j['doi'], doi, isDOI1=True, isDOI2=True)
                    else:
                        dbcon.link_ref(j['title'], doi,
                                       isDOI1=False, isDOI2=True)
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


DOIS = load_dataset.get_dois()
for i in DOIS:
    l = rec(i, 2, l, dbcon)
    print(len(l))

dbcon.close()
