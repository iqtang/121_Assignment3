import re
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer

weights = {
    "title": 3, "h1":3, "h2":2, "h3":2, "b":1.5, "strong":1.5
}

def tokenize(data):
    content = data.get("content")
    soup = BeautifulSoup(content, "html.parser")
    stemmer = PorterStemmer()

    weighted_tokens = []
    for tag, weight in weights.items():
        for element in soup.find_all(tag):
            words = re.findall(r'\b[a-zA-Z0-9_]+\b', element.get_text().lower())
            for word in words:
                weighted_tokens.append((stemmer.stem(word), weight))

    text = soup.get_text()
    for line in text.splitlines():
        line = line.lower()
        line = re.sub(r'[^a-zA-Z0-9]', " ", line)
        words = re.findall(r'\b[a-zA-Z0-9_]+\b', line)
        for word in words:
            weighted_tokens.append((stemmer.stem(word), 1))
    return weighted_tokens

def computeWordFrequencies(tokens):
    frequencies = {}
    for token, weight in tokens:
        if token in frequencies:
            frequencies[token] += weight
        else:
            frequencies[token] = 1
    return frequencies