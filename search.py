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





if __name__ == "__main__":
    inverted_index = {
        "cristina": {1: (3, 0.0035),2: (1, 0.0023)},
        "lopes": {1: (2, 0.0023)},
        "machine": {2: (2, 0.0046),3: (1, 0.0016)},
        "learning": {2: (1, 0.0023),3: (2, 0.0032)},
        "acm": {1: (1, 0.0012),3: (1, 0.0016)},
        "master": {4: (2, 0.0026)},
        "of": {4: (2, 0.0026)},
        "software": {4: (3, 0.0040)},
        "engineering": {4: (1, 0.0013)}
    }

    engine = SearchEngine(inverted_index)
    queries = ["cristina lopes", "machine learning", "ACM", "master of software engineering"]
    print("\n--- Running milestone queries ---")
    for q in queries:
        print(f"\nQuery: '{q}'")
        results = engine.search(q)
        if results:
            print(f"Top {min(5, len(results))} results:")
            for idx, (doc_id, url, score) in enumerate(results[:5], start=1):
                print(f"{idx}. DocID: {doc_id}, URL: {url}, Score: {score}")
        else:
            print("No results found.")

    print("\n--- Query Search ---")
    print("Type your query and press Enter.")
    print("Type 'exit' to quit.\n")

    while True:
        query = input("Enter your search query: ")
        if query.lower() == 'exit':
            print("Goodbye!")
            break
        results = engine.search(query)
        if results:
            print(f"\nTop {min(5, len(results))} results for '{query}':")
            for idx, (doc_id, url, score) in enumerate(results[:5], start=1):
                print(f"{idx}. DocID: {doc_id}, URL: {url}, Score: {score}")
        else:
            print(f"No results found for '{query}'.\n")