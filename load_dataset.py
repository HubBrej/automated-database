import bibtexparser
from bibtexparser.bparser import BibTexParser
import os


def get_data():

    TEXT_DATA_DIR = os.path.join(
        "C:/Users/Hubert.DESKTOP-GR3P7N2/Documents/PRI-base-articles-crypto/Classification/training_data")
    print('Processing text dataset')

    dois = []
    titles = []
    labels_index = {}  # dictionary mapping label name to numeric id
    labels = []  # list of label ids

    path = os.path.join(
        "C:/Users/Hubert.DESKTOP-GR3P7N2/Documents/PRI-base-articles-crypto/Classification/training_data/Crypto")
    if os.path.isdir(path):
        for fname in sorted(os.listdir(path)):
            fpath = os.path.join(path, fname)
            with open(fpath) as bibtex_file:
                parser = BibTexParser(interpolate_strings=False)
                bib_database = bibtexparser.load(bibtex_file, parser)
                for publi in bib_database.entries:
                    if "doi" in publi:
                        doi = publi['doi']
                        dois.append(doi)
                    else :
                        if "title" in publi:
                            titles.append(publi['title'])

    dois = [x.replace("\\", "") for x in dois]

    return dois, titles
