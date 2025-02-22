import pathlib
import json
from collections import defaultdict
from tokenizer import *

dev_path = pathlib.Path("/Users/delaneyharwell/DEV")
output_file = "index.txt"

partial_index = defaultdict(list)
docID_map = dict()
NUM_DOCS = 0
SAVE_INTERVAL = 50


def save_index_to_file():
    try:
        with open(output_file, "w") as index_file:
            for word, freq in partial_index.items():
                index_file.write("{}\t{}\n".format(word, freq))
        partial_index.clear()
        print("Saved 50 index entries to output file")
    except FileNotFoundError:
        print("Index file not found")
        return


def main():
    global NUM_DOCS
    counter = 0
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
                save_index_to_file()
    if partial_index:
        save_index_to_file()



if __name__ == '__main__':
    main()
