import pathlib
import json
import heapq
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
    write_buffer = "index.json"

    read_buffers = []
    for json_file in partial_path.rglob("*.json"):
        with open(json_file, "r") as file:
            read_buffers.append(file)




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



if __name__ == '__main__':
    main()
