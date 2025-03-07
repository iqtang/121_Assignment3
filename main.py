import search
from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
Engine = search.SearchEngine("index.json")

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query').lower()
    if not query:
        return jsonify({"error": "No query provided"})
    results = Engine.search(query)
    results = [result[0] for result in results]
    return jsonify({"results": results})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5003,debug=True)
