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

def calculate_tf_idf_list(terms, index_data, url = None):
    res = []

    for term in terms:
        if url: tf = index_data[term][url[0]][1]
        else: tf = terms.count(term) / len(terms)

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
    print(f"URL TF-IDFS -----> {url_tfs}")
    term_tfs = calculate_tf_idf_list(terms, index_data)
    print(f"QUERY TF-IDFS -----> {term_tfs}")

    similarities = [cosine_sim(term_tfs, tf) for tf in url_tfs]
    indexes = np.argsort(similarities)
    return [urls[index] for index in indexes[::-1]]




