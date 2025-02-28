import json
from collections import defaultdict
import pathlib

NUM_TERMS = 1094910
NUM_DOCS = 55393

def calculate_tfidf(posting):
    for docid, freq in posting:




def get_tf_idfs():
    global NUM_TERMS

    tf_idfs = defaultdict(float)
    index_range_path = pathlib.Path("index_ranges")

    for json_file in index_range_path.rglob("*.json"):
        with open(json_file, 'r') as file:
            index = json.load(file)
            for word, postings in index.items():



