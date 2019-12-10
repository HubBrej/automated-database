from neo4j import GraphDatabase


class Dbcon(object):

    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def create_author(self, name):
        with self._driver.session() as session:
            session.run("MERGE (:Author {name: $name})", name=name)

    def create_topic(self, name):
        with self._driver.session() as session:
            session.run("MERGE (:Topic {name: $name})", name=name)

    def create_publi(self, title, doi, year):
        with self._driver.session() as session:
            session.run(
                "MERGE (:Publication {title: $title, doi: $doi, year: $year})", title=title, doi=doi, year=year)

    def link_auth_publi(self, author, publication, isDOI=True):
        if isDOI:
            with self._driver.session() as session:
                session.run("MERGE (a:Author {name: $author})"
                            "MERGE (p:Publication {doi: $publication})"
                            "MERGE (a)-[:WROTE]->(p)", author=author, publication=publication)
        else:
            with self._driver.session() as session:
                session.run("MERGE (a:Author {name: $author})"
                            "MERGE (p:Publication {title: $publication})"
                            "MERGE (a)-[:WROTE]->(p)", author=author, publication=publication)

    def link_top_publi(self, topic, publication, isDOI=True):
        if isDOI:
            with self._driver.session() as session:
                session.run("MERGE (t:Topic {name: $topic})"
                            "MERGE (p:Publication {doi: $publication})"
                            "MERGE (p)-[:RELATED]->(t)", topic=topic, publication=publication)
        else:
            with self._driver.session() as session:
                session.run("MERGE (t:Topic {name: $topic})"
                            "MERGE (p:Publication {title: $publication})"
                            "MERGE (p)-[:RELATED]->(t)", topic=topic, publication=publication)

    def link_ref(self, publi1, publi_cited, isDOI1=True, isDOI2=True):
        if isDOI1 and isDOI2:
            with self._driver.session() as session:
                session.run("MERGE (t:Publication {doi: $publi1})"
                            "MERGE (p:Publication {doi: $publi_cited})"
                            "MERGE (t)-[:CITE]->(p)", publi1=publi1, publi_cited=publi_cited)
        if isDOI1 and not isDOI2:
            with self._driver.session() as session:
                session.run("MERGE (t:Publication {doi: $publi1})"
                            "MERGE (p:Publication {title: $publi_cited})"
                            "MERGE (t)-[:CITE]->(p)", publi1=publi1, publi_cited=publi_cited)
        if not isDOI1 and isDOI2:
            with self._driver.session() as session:
                session.run("MERGE (t:Publication {title: $publi1})"
                            "MERGE (p:Publication {doi: $publi_cited})"
                            "MERGE (t)-[:CITE]->(p)", publi1=publi1, publi_cited=publi_cited)
        if not isDOI1 and not isDOI2:
            with self._driver.session() as session:
                session.run("MERGE (t:Publication {title: $publi1})"
                            "MERGE (p:Publication {title: $publi_cited})"
                            "MERGE (t)-[:CITE]->(p)", publi1=publi1, publi_cited=publi_cited)

    def link_aliases(self, auth1, auth2):
        with self._driver.session() as session:
            session.run("MERGE (t:Author {name: $auth1})"
                        "MERGE (p:Author {name: $auth2})"
                        "MERGE (p)-[:ALIAS]->(t)", auth1=auth1, auth2=auth2)
