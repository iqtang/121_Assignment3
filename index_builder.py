import pathlib
import json
import heapq
import ijson
import os
from collections import defaultdict
from tokenizer import *

dev_path = pathlib.Path("developer")
partial_path = pathlib.Path("partial_indices")
output_file = "index.json"

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
        sorted_index = {word: sorted(postings, key=lambda x: x[0]) for word, postings in sorted(partial_index.items())}

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

    '''
    merged_index = defaultdict(list)
    heap = []
    read_buffers = []

    for json_file in partial_path.rglob("*.json"):
        file = open(json_file, "r")
        read_buffers.append(ijson.parse(file))

        for prefix, event, value in read_buffers[0]:
            if event == "map_key":
                print(value)
    '''


def split_index():
    ranges = {"0-4", "5-9", "a-m", "n-z"}
    range_posting = defaultdict(None)



    index = defaultdict(list)
    with open("index.json", "r") as file:
        index = json.load(file)


    current_range = "0-4"
    for word, posting in index.items():
        first_char = word[0].lower()

        new_range = get_range(first_char)

        if new_range != current_range:
            with open(f"index_ranges/index[{current_range}]", "w") as file:
                json.dump(range_posting, file)

            range_posting.clear()
            current_range = new_range

        range_posting[word] = posting

def get_range(character):
    if '0' <= character <= '4':
        return "0-4"
    elif '5' <= character <= '9':
        return "5-9"
    elif 'a' <= character <= 'm':
        return "a-m"
    elif 'n' <= character <= 'z':
        return "n-z"
    else:
        return None


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
    split_index()


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
