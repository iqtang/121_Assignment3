import pathlib
import json
from collections import defaultdict

from tokenizer import *

dev_path = pathlib.Path("developer")

docID_map = dict()
NUM_DOCS = 0


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

            if counter >= 10:
                break


if __name__ == '__main__':
    main()
