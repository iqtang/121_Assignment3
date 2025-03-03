import os
import re
import json
from index_builder import get_range
from nltk.stem import PorterStemmer
from ranking import get_rankings

def categorize_tokens(terms):
    categories = {'0-4': [], '5-9': [], 'a-m': [], 'n-z': []}

    for term in terms:
        token_range = get_range(term[0])
        categories[token_range].append(term)

    return categories



class SearchEngine:
    def __init__(self, inverted_index):
        self.inverted_index = inverted_index

    def search(self, query):
        try:
            with open('docID_data/docIDmap.json', "r") as f:
                docID_map = json.load(f)
        except FileNotFoundError:
            return []

        stemmer = PorterStemmer()
        query = query.lower()
        query = re.sub(r'[^a-zA-Z0-9]', " ", query)
        terms = re.findall(r'\b[a-zA-Z0-9_]+\b', query)
        terms = [stemmer.stem(word) for word in terms]
        if not terms:
            return []

        categorized_terms = categorize_tokens(terms)
        index_data = inverted_index
        '''
        for term_range, term_list in categorized_terms.items():
            if term_list:
                partial_index_path = f"index_ranges/index[{term_range}]"
                if os.path.exists(partial_index_path):
                    with open(partial_index_path, "r") as f:
                        index_data.update(json.load(f))
        '''
        doc_sets = []
        for term in terms:
            doc_set = set(index_data.get(term, {}).keys())
            if not doc_set:
                return []
            doc_sets.append(doc_set)
        result_docs = set.intersection(*doc_sets) if doc_sets else set() #returns only the documents that have all the query terms
        urls =  [(result, docID_map[str(result)][0]) for result in result_docs]
        return get_rankings(terms, index_data, urls)

import os
import re
import json
from index_builder import get_range
from nltk.stem import PorterStemmer
from ranking import get_rankings


def categorize_tokens(terms):
    categories = {'0-4': [], '5-9': [], 'a-m': [], 'n-z': []}

    for term in terms:
        token_range = get_range(term[0])
        categories[token_range].append(term)

    return categories


class SearchEngine:
    def __init__(self, inverted_index):
        self.inverted_index = inverted_index

    def search(self, query):
        try:
            with open('docID_data/docIDmap.json', "r") as f:
                docID_map = json.load(f)
        except FileNotFoundError:
            return []

        stemmer = PorterStemmer()
        query = query.lower()
        query = re.sub(r'[^a-zA-Z0-9]', " ", query)
        terms = re.findall(r'\b[a-zA-Z0-9_]+\b', query)
        terms = [stemmer.stem(word) for word in terms]
        if not terms:
            return []

        categorized_terms = categorize_tokens(terms)
        index_data = self.inverted_index

        doc_sets = []
        for term in terms:
            doc_set = set(index_data.get(term, {}).keys())
            if not doc_set:
                return []
            doc_sets.append(doc_set)
        result_docs = set.intersection(*doc_sets) if doc_sets else set()
        urls = [(result, docID_map[str(result)][0]) for result in result_docs]
        return get_rankings(terms, index_data, urls)


def run_queries(engine):
    queries = ["cristina lopes", "machine learning", "ACM", "master of software engineering"]
    print("\n--- Running milestone queries ---")
    for q in queries:
        print(f"\nQuery: '{q}'")
        results = engine.search(q)
        if results:
            print(f"{len(results)} results:")
            for idx, (doc_id, url, score) in enumerate(results, start=1):
                print(f"{idx}. DocID: {doc_id}, URL: {url}, Score: {score}")
        else:
            print("No results found.")


def write_report(engine, filename="report.txt"):
    queries = ["cristina lopes", "machine learning", "ACM", "master of software engineering"]
    with open(filename, "w") as report_file:
        report_file.write("Search Report\n")
        report_file.write("===========================\n\n")
        for q in queries:
            report_file.write(f"Query: '{q}'\n")
            results = engine.search(q)
            if results:
                top_results = results[:5]
                for idx, (doc_id, url, score) in enumerate(top_results, start=1):
                    report_file.write(f"{idx}. DocID: {doc_id}, URL: {url}, Score: {score}\n")
            else:
                report_file.write("No results found.\n")
            report_file.write("\n")
    print(f"\nReport written to '{filename}'.")


if __name__ == "__main__":
    inverted_index = {
        "cristina": {1: (3, 0.0035), 2: (1, 0.0023)},
        "lopes": {1: (2, 0.0023)},
        "machine": {2: (2, 0.0046), 3: (1, 0.0016)},
        "learning": {2: (1, 0.0023), 3: (2, 0.0032)},
        "acm": {1: (1, 0.0012), 3: (1, 0.0016)},
        "master": {4: (2, 0.0026)},
        "of": {4: (2, 0.0026)},
        "software": {4: (3, 0.0040)},
        "engineering": {4: (1, 0.0013)}
    }

    engine = SearchEngine(inverted_index)

    run_queries(engine)
    write_report(engine)