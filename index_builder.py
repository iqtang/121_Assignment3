import pathlib
import json
import heapq
import ijson
import os
from collections import defaultdict
from tokenizer import *
from ranking import calculate_tf

dev_path = pathlib.Path("developer")
partial_path = pathlib.Path("partial_indices")
output_file = "index.json"

unique_words = set()
docID_map = dict()
NUM_DOCS = 0
SAVE_INTERVAL = 2000

PARTIAL_INDEX_COUNTER = 1

def add_to_map(data):
    content = data.get("content")
    soup = BeautifulSoup(content, "html.parser")

    text = soup.get_text()
    re.sub(r'[^a-zA-Z0-9]', " ", text)
    words = re.findall(r'\b[a-zA-Z0-9_]+\b', text)
    docID_map[NUM_DOCS] = (data.get("url"), len(words))

def save_index_to_file(partial_index):
    global PARTIAL_INDEX_COUNTER

    partial_index_path =  f"partial_indices/partial_index_{PARTIAL_INDEX_COUNTER}.json"
    PARTIAL_INDEX_COUNTER += 1
    try:

        with open(partial_index_path, 'w') as file:
            json.dump(partial_index, file)

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
            #docID_map[NUM_DOCS] = (data.get("url"))
            #creares a docID map with the values being a tuple containing a
            #url as well as the number of words in the page.

            add_to_map(data)
            tokens = tokenize(data)
            word_frequencies = computeWordFrequencies(tokens)

            for word, freq in word_frequencies.items():
                partial_index[word][NUM_DOCS] = (freq, calculate_tf(freq, docID_map[NUM_DOCS]))

            if counter % SAVE_INTERVAL == 0:
                save_index_to_file(partial_index)
                partial_index.clear()

    if partial_index:
        save_index_to_file(partial_index)

    if docID_map:
        with open("docID_data/docIDmap.json", "w") as f:
            json.dump(docID_map, f)

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
