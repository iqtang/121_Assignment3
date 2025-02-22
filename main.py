import pathlib
import json
from tokenizer import *

dev_path = pathlib.Path("developer")


def main():
    for json_file in dev_path.rglob("*.json"):
        with open(json_file, 'r') as file:
            data = json.load(file)

            tokens = tokenize(data)


if __name__ == '__main__':
    main()
