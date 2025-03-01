from nltk.stem import PorterStemmer
import re
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
        doc_set = []
        for term in terms:
            if term in self.inverted_index:
                doc_set.append(set(self.inverted_index[term].keys()))
            else:
                return []
                #return []? missing chunk of query in index table so how to proceed?
        result_docs = set.intersection(*doc_set) #returns only the documents that have all the qery terms
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
