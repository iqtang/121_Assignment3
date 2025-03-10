from search import *
from flask import Flask, request, jsonify
from flask_cors import CORS
from ranking import *
import search
from txt_retrieval import *
'''app = Flask(__name__)
CORS(app)


@app.route('/search', methods=['GET'])
def search():
    with open('docID_data/docIDmap.json', "r") as f:
        docID_map = json.load(f)
    query = request.args.get('query').lower()
    if not query:
        return jsonify({"error": "No query provided"})
    offsets = get_offsets("final_index.txt")
    engine = SearchEngine("final_index.txt", offsets)
    results = engine.search(query, docID_map)
    return jsonify({"results": results})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5004,debug=True)'''
# import search
# from txt_retrieval import get_offsets
#
#
if __name__ == '__main__':
    offsets = get_offsets("final_index.txt")
    engine = search.SearchEngine("final_index.txt", offsets)
    print("Welcome to the search engine!\nEnter your search query or 'exit' to exit.")
    search.runner(engine)
    print("Thank you for searching!")
     #search.write_report(engine)'''