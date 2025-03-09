import pathlib
import json
from collections import defaultdict, OrderedDict

def convert_to_txt(txt_path, json_path):
    data = defaultdict(list)
    with open(txt_path, "a") as text_file:
        with open(json_path, 'r') as file:
            data = json.load(file)
            data = OrderedDict(sorted(data.items()))
            print(f"Dictionary Length: {len(data)}")

        for term, posting in data.items():
            text_file.write(f"{term}: {str(posting)}\n")

def create_index():
    range_path = pathlib.Path("index_ranges")
    for json_file in range_path.rglob('*'):
        convert_to_txt("final_index.txt", json_file)


def get_offsets(index_path):
    byte_offsets = {}

    with open(index_path, 'rb') as file:
        current_offset = 0

        while True:
            line = file.readline()
            if not line:
                break

            # Get the term from the line (assuming "term: posting" format)
            term = line.split(b":")[0].decode('utf-8')

            # Store the byte offset where this term starts
            byte_offsets[term] = current_offset

            # Update the current byte offset by adding the length of the current line
            current_offset += len(line)

    return byte_offsets


def retrieve_data(query, index_path, offsets):
    result = {}
    with open(index_path, 'r') as file:
        for word in query:
            if word in offsets:
                file.seek(offsets[word])

                line = file.readline()

                term, data_str = line.strip().split(': ', 1)
                data_str = data_str.replace("'", '"')
                data = json.loads(data_str)
                result[term] = data

    return result



if __name__ == '__main__':
    create_index()



