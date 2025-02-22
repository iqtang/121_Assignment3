import re
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer


def tokenize(data):
    tokens = []
    content = data.get("content")
    soup = BeautifulSoup(content, "html.parser")

    text = soup.get_text()

    for line in text.splitlines():
        line = line.lower()
        line = re.sub(r'[^a-zA-Z0-9]', " ", line)
        tokens.extend(re.findall(r'\b[a-zA-Z0-9_]+\b', line))

    stemmer = PorterStemmer()

    stems = [stemmer.stem(token) for token in tokens]

    return stems

def computeWordFrequencies(tokens):
    frequencies = {}
    for token in tokens:
        if token in frequencies:
            frequencies[token] += 1
        else:
            frequencies[token] = 1

    return frequencies