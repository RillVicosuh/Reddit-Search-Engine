import lucene
import os
from org.apache.lucene.store import MMapDirectory, SimpleFSDirectory, NIOFSDirectory
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig, IndexOptions, DirectoryReader
from org.apache.lucene.search import IndexSearcher, BoostQuery, Query
from org.apache.lucene.search.similarities import BM25Similarity
from flask import request, Flask, render_template, url_for, redirect
from pylucene import retrieve

app = Flask(__name__)

# Initialize the Lucene JVM
#lucene.initVM(vmargs=['-Djava.awt.headless=true'])

# Define the route for search functionality
@app.route('/', methods=['POST', 'GET'])
def home():
    if request.method == "POST":
        query = request.form["query"]
        return redirect(url_for("output", qry=query))
    else:
        return render_template("index.html")

# Define the route for the output functionality
@app.route("/<qry>", methods=['POST', 'GET'])
def output(qry):
   # query = request.form['query']  # Get the user-entered query from the form
    query = qry
    lucene.getVMEnv().attachCurrentThread()
    results = retrieve('reddit_index/', query)  # Call the retrieve function to get the search results
    return render_template('results.html', **locals())

if __name__ == "__main__":
    app.run(debug=True)
