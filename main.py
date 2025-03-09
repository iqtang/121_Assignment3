import search
from txt_retrieval import get_offsets


if __name__ == '__main__':
    offsets = get_offsets("final_index.txt")
    engine = search.SearchEngine("final_index.txt", offsets)
    print("Welcome to the search engine!\nEnter your search query or 'exit' to exit.")
    search.runner(engine)
    print("Thank you for searching!")
    #search.write_report(engine)