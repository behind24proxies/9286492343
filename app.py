
from flask import Flask, jsonify, request, Response
from ml_news_core import google_news_search
import json
import os
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
@app.route("/")
def index():
    return "Machine Learning API for Balanced News Summary" 

@app.route("/ml-related-news",methods=["GET"])
def api():
    args = request.args
    attempts = 0
    if "url" in args:
        results = google_news_search(args["url"])
        return jsonify(results)
        
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, port=port)