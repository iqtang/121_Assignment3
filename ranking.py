import json
from collections import defaultdict
import pathlib

NUM_TERMS = 1094910
NUM_DOCS = 55393

def calculate_tfidf(posting):
    #TF(t,d) = (Num term t appears in document d) / (total # terms in doc d)
    #IDF{t, D) = log((total # of docs in corpus D) / (num doc containing term t)
    #TF-IDF(t, d, D) = TF(t,d)*IDF(t,D)
    for docid, freq in posting:




def get_tf_idfs():
    global NUM_TERMS

    tf_idfs = defaultdict(float)
    index_range_path = pathlib.Path("index_ranges")

    for json_file in index_range_path.rglob("*.json"):
        with open(json_file, 'r') as file:
            index = json.load(file)
            for word, postings in index.items():



