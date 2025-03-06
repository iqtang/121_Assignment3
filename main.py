import search


if __name__ == '__main__':
    engine = search.SearchEngine("index.json")
    print("Welcome to the search engine!\nEnter your search query or 'exit' to exit.")
    search.runner(engine)
    print("Thank you for searching!")
    search.write_report(engine)