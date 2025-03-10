import json
import math
import numpy as np

from collections import defaultdict
import pathlib

NUM_TERMS = 1094910
#NUM_DOCS = 55393
NUM_DOCS = 4


def cosine_sim(x, y):
    return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))

def calculate_tf(freq, mapVal):
    #TF(t,d) = (Num term t appears in document d) / (total # terms in doc d)
    #IDF{t, D) = log((total # of docs in corpus D) / (num doc containing term t)
    #TF-IDF(t, d, D) = TF(t,d)*IDF(t,D)

    return freq / mapVal[1]

def set_tf_idfs(index):
    for term, posting in index.items():
        idf = NUM_DOCS / len(index[term])
        for doc, data in posting.items():
            data[1] = math.log(data[1] / idf)

        print(f"\nSET TF-IDFs FOR {term}\n")

def calculate_tf_idf_list(terms, index_data, url = None):
    res = []

    for term in terms:
        if url:
            if url[0] in index_data[term].keys():
                res.append(index_data[term][url[0]][1])
            else:
                res.append(0)
        else:
            tf = terms.count(term) / len(terms)
            idf = NUM_DOCS / len(index_data[term])
            res.append(math.log(tf / idf))

    return res


def get_tf_idfs(terms, index_data, urls):
    res = []
    for url in urls:
        res.append(calculate_tf_idf_list(terms, index_data, url))

    return res


def get_rankings(terms, index_data, urls):
    url_tfs = get_tf_idfs(terms, index_data, urls)
    term_tfs = calculate_tf_idf_list(terms, index_data)

    similarities = [cosine_sim(term_tfs, tf) for tf in url_tfs]
    indexes = np.argsort(similarities)
    result = [urls[index] for index in indexes[::-1]]
    return result




