import os

from nltk.stem import PorterStemmer
import re
import json
from index_builder import get_range, docID_map

def categorize_tokens(terms):
    categories = {'0-4': [], '5-9': [], 'a-m': [], 'n-z': []}

    for term in terms:
        range = get_range(term)
        categories[range].append(term)

    return categories



class SearchEngine:
    def __init__(self, inverted_index):
        self.inverted_index = inverted_index

    def search(self, query):
        stemmer = PorterStemmer()
        query = query.lower().split()
        query = re.sub(r'[^a-zA-Z0-9]', " ", query)
        terms = re.findall(r'\b[a-zA-Z0-9_]+\b', query)
        terms = [stemmer.stem(word) for word in terms]
        if not terms:
            return []

        categorized_terms = categorize_tokens(terms)
        index_data = {}
        for term_range, term_list in categorized_terms.items():
            if term_list:
                partial_index_path = f"index_ranges/index[{term_range}]"
                if os.path.exists(partial_index_path):
                    with open(partial_index_path, "r") as f:
                        index_data.update(json.load(f))
        doc_sets = []
        for term in terms:
            doc_set = set(index_data.get(term, {}).keys())
            if not doc_set:
                return []
            doc_sets.append(doc_set)
        result_docs = set.intersection(*doc_sets) if doc_sets else set() #returns only the documents that have all the qery terms
        return [docID_map[result] for result in result_docs]





if __name__ == "__main__":
    inverted_index = {
        'cristina': {1: 3, 2: 1},
        'lopes': {1: 2},
        'machine': {2: 2, 3: 1},
        'learning': {2: 1, 3: 2},
        'acm': {1: 1, 3: 1},
        'master': {4: 2},
        'of': {4: 2},
        'software': {4: 3},
        'engineering': {4: 1}
    }
    engine = SearchEngine(inverted_index)
    queries = ["christina lopes", "machine learning", "ACM", "master of software engineering"]
    for q in queries:
        results = engine.search(q)
        for r in results:
            print(r)
