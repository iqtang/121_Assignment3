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
        result_docs = set.intersection(
            *doc_sets) if doc_sets else set()  # returns only the documents that have all the query terms
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
                print(f"{idx}. DocID: {doc_id}, URL: {url[1]}, Score: {score}")
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

def runner(search_engine):
    while True:
        inp = input("\nSearch query: ")
        if inp.lower() == "exit":
            break
        print(f"\nQuery: '{inp.strip()}'")
        results = search_engine.search(inp.strip())
        if results:
            print(f"{len(results)} results:\n")
            for idx, url in enumerate(results, start=1):
                print(f"{idx}. URL: {url[1]}")
        else:
            print("No results found.")


if __name__ == "__main__":
    se = SearchEngine("Inverted Index")
    runner(se)