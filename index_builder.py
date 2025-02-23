import pathlib
import json
import heapq
import os
from collections import defaultdict
from tokenizer import *

dev_path = pathlib.Path("developer")
partial_path = pathlib.Path("partial_indices")
output_file = "index.txt"

unique_words = set()
docID_map = dict()
NUM_DOCS = 0
SAVE_INTERVAL = 2000

PARTIAL_INDEX_COUNTER = 1


def save_index_to_file(partial_index):
    global PARTIAL_INDEX_COUNTER

    partial_index_path =  f"partial_indices/partial_index_{PARTIAL_INDEX_COUNTER}.json"
    PARTIAL_INDEX_COUNTER += 1
    try:
        sorted_index = {word: sorted(postings, key=lambda x: x[0]) for word, postings in partial_index.items()}

        with open(partial_index_path, 'w') as file:
            json.dump(sorted_index, file)

    except FileNotFoundError:
        print("Index file not found")
        return


def merge_indices():
    final_index = defaultdict(list)

    for json_file in partial_path.rglob("*.json"):
        with open(json_file, "r") as file:
            partial_index = json.load(file)
            for word, postings in partial_index.items():
                final_index[word].extend(postings)

    # Sort postings lists
    for word in final_index:
        final_index[word] = sorted(final_index[word], key=lambda x: x[0])

    # Save final index
    with open(output_file, "w") as file:
        json.dump(final_index, file)

    print("Index merged and saved successfully.")

    return final_index




def main():
    global NUM_DOCS

    counter = 0
    partial_index = defaultdict(list)

    for json_file in dev_path.rglob("*.json"):
        counter += 1
        with open(json_file, 'r') as file:
            NUM_DOCS += 1
            data = json.load(file)
            docID_map[NUM_DOCS] = data.get("url")
            tokens = tokenize(data)
            word_frequencies = computeWordFrequencies(tokens)

            for word, freq in word_frequencies.items():
                partial_index[word].append((NUM_DOCS, freq))

            if counter % SAVE_INTERVAL == 0:
                save_index_to_file(partial_index)
                partial_index.clear()

    if partial_index:
        save_index_to_file(partial_index)
    final_index = merge_indices()
    generate_report(final_index)


def generate_report(final_index):
    num_tokens = len(final_index)
    index_size = os.path.getsize(output_file) / 1024  # KB

    report_data = f"""
    Inverted Index Report
    ----------------------
    Number of documents indexed: {NUM_DOCS}
    Number of unique tokens: {num_tokens}
    Total size of the index on disk: {index_size:.2f} KB
    """

    with open("report.txt", "w") as report_file:
        report_file.write(report_data)

    print("Report generated successfully.")


if __name__ == '__main__':
    main()
