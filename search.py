import os
import re
import json
from index_builder import get_range
from nltk.stem import PorterStemmer
from ranking import get_rankings
from collections import Counter

stop_words = [
    "a", "an", "and", "are", "as", "at", "be", "but", "by", "for", "if", "in", "into", "is", "it", "no", "not",
    "of", "on", "or", "such", "that", "the", "their", "then", "there", "these", "they", "this", "to", "was",
    "will", "with", "you"
]



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
        terms = [stemmer.stem(word) for word in terms if word not in stop_words]
        if not terms:
            return []

        categorized_terms = categorize_tokens(terms)
        index_data = {}
        doc_counter = Counter()

        for term_range, term_list in categorized_terms.items():
            if term_list:
                partial_index_path = f"index_ranges/index[{term_range}]"
                if os.path.exists(partial_index_path):
                    with open(partial_index_path, "r") as f:
                        index_data.update(json.load(f))
        doc_sets = []
        for term in terms:
            doc_set = index_data.get(term, {})
            if not doc_set:
                return []
            doc_counter.update(doc_set[0])
        result_docs = sorted(doc_counter.items(), key=lambda x: x[1], reverse=True)
        return [docID_map[str(result_doc[0])] for result_doc in result_docs]

def run_queries(engine):
    queries = ["cristina lopes", "machine learning", "ACM", "master of software engineering"]
    print("\n--- Running milestone queries ---")
    for q in queries:
        print(f"\nQuery: '{q}'")
        results = engine.search(q)
        if results:
            print(f"{len(results)} results:\n")
            for idx, (doc_id, url) in enumerate(results, start=1):
                print(f"{idx}. URL: {doc_id}, docID: {url}")
        else:
            print("No results found.")

def runner(engine):
    while True:
        inp = input("\nSearch query: ")
        if inp.lower() == "exit":
            break
        print(f"\nQuery: '{inp.strip()}'")
        results = engine.search(inp.strip())
        if results:
            print(f"{len(results)} results:\n")
            for idx, (doc_id, url) in enumerate(results, start=1):
                print(f"{idx}. URL: {doc_id}, DocID: {url}")
        else:
            print("No results found.")


def write_report(engine, filename="search_report.txt"):
    queries = ["cristina lopes", "machine learning", "ACM", "master of software engineering"]
    with open(filename, "w") as report_file:
        report_file.write("Search Report\n")
        report_file.write("===========================\n\n")
        for q in queries:
            report_file.write(f"Query: '{q}'\n")
            results = engine.search(q)
            if results:
                top_results = results[:5]
                for idx, (doc_id, url) in enumerate(top_results, start=1):
                    report_file.write(f"{idx}. DocID: {doc_id}, URL: {url}\n")
            else:
                report_file.write("No results found.\n")
            report_file.write("\n")
    print(f"\nReport written to '{filename}'.")


if __name__ == "__main__":
    pass
    # engine = SearchEngine("/index_data/index.txt")
    # runner(engine)
    # # run_queries(engine)
    # write_report(engine)