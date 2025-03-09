import pathlib
import json
import os
from collections import defaultdict
from tokenizer import *
from ranking import calculate_tf, set_tf_idfs

dev_path = pathlib.Path("developer/DEV")
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
    os.makedirs(partial_path, exist_ok = True)

    partial_index_path =  f"partial_indices/partial_index_{PARTIAL_INDEX_COUNTER}.json"
    PARTIAL_INDEX_COUNTER += 1
    sorted_index = {
        key: {doc_id: value for doc_id, value in sorted(nested_dict.items())}
        for key, nested_dict in sorted(partial_index.items())
    }

    print(sorted_index)

    try:
        with open(partial_index_path, 'w') as file:
            json.dump(sorted_index, file)


    except FileNotFoundError:
        print("Index file not found")
        return


def merge_indices():
    final_index = defaultdict(dict)

    for json_file in partial_path.rglob("*.json"):
        with open(json_file, "r") as file:
            partial_index = json.load(file)
            for word, postings in partial_index.items():
                final_index[word].update(postings)

    # Save final index
    with open(output_file, "w") as file:
        json.dump(final_index, file)

    print("Index merged and saved successfully.")

    return final_index


def split_index():
    os.makedirs("index_ranges", exist_ok = True)
    range_posting = defaultdict(None)

    print("LOADING JSON...")
    with open("index.json", "r") as file:
        index = json.load(file)

    print("JSON LOADED!\n")


    current_range = "0-4"
    print(f"CURRENT RANGE ->>> {current_range}")
    for word, posting in index.items():
        first_char = word[0].lower()

        new_range = get_range(first_char)

        if new_range != current_range:
            try:
                with open(f"index_ranges/index[{current_range}]", "r") as f:
                    existing_index = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                existing_index = {}

            existing_index.update(range_posting)

            with open(f"index_ranges/index[{current_range}]", "w") as file:
                json.dump(existing_index, file)

            range_posting.clear()
            existing_index.clear()
            current_range = new_range
            print(f"\n\nRANGE NOW ---> {current_range}\n")

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
    partial_index = defaultdict(dict)

    for json_file in dev_path.rglob("*.json"):
        print(f"CURRENT -> {json_file}")
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
                partial_index[word][NUM_DOCS] = [freq, calculate_tf(freq, docID_map[NUM_DOCS])]

            if counter % SAVE_INTERVAL == 0:
                save_index_to_file(partial_index)
                partial_index.clear()
            print(f"DONE with: {json_file}")

    if partial_index:
        save_index_to_file(partial_index)

    if docID_map:
        os.makedirs("docID_data", exist_ok = True)
        with open("docID_data/docIDmap.json", "w") as f:
            json.dump(docID_map, f)

    final_index = merge_indices()
    generate_report(final_index)
    set_tf_idfs(final_index)
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
