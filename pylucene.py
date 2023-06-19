import json
import os
import flask
import lucene
from datetime import datetime
from java.nio.file import Paths
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import (
    FieldInfo,
    IndexWriter,
    IndexWriterConfig,
    IndexOptions,
    DirectoryReader,
)
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.search.similarities import BM25Similarity


# Initialize lucene and JVM
lucene.initVM(vmargs=['-Djava.awt.headless=true'])

def create_index(directory, index_dir):
    # Check if the directory for the index exists, if not, create it
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    
    # Initialize directory to store index and an analyzer
    store = SimpleFSDirectory(Paths.get(index_dir))
    analyzer = StandardAnalyzer()
    
    # Configure index writer
    config = IndexWriterConfig(analyzer)
    config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
    writer = IndexWriter(store, config)

    # Define the FieldTypes for the index
    metaType = FieldType() # for metadata fields
    metaType.setStored(True)
    metaType.setTokenized(False)
    
    contextType = FieldType() # for content fields
    contextType.setStored(True)
    contextType.setTokenized(True)
    contextType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)

    # Iterate over all .jsonl files in the given directory
    for filename in os.listdir(directory):
        if filename.endswith('.jsonl'):
            with open(os.path.join(directory, filename), 'r') as f:
                # For each line in the file (each post)
                for line in f:
                    data = json.loads(line)

                    # Create a Document for the post
                    doc = Document()
                    doc.add(Field('id', data['id'], metaType))
                    doc.add(Field('author', data['author'], metaType))
                    doc.add(Field('title', data['title'], contextType))
                    doc.add(Field('body', data['selftext'], contextType))
                    doc.add(Field('url', data['url'], metaType))
                    doc.add(Field('permalink', data['permalink'], metaType))
                    doc.add(Field('created_utc', datetime.utcfromtimestamp(data['created_utc']).isoformat(), metaType))

                    # Add each comment as a separate field in the Document
                    for comment in data['comments']:
                        doc.add(Field('comment', comment['body'], contextType))

                    # Add the Document to the index
                    writer.addDocument(doc)

    # Close the index writer
    writer.close()

def retrieve(index_dir, query):
    # Open the index directory
    search_dir = SimpleFSDirectory(Paths.get(index_dir))
    #IndexSearcher automatically calculates the score for a doc and the default is BM_25
    searcher = IndexSearcher(DirectoryReader.open(search_dir))
    #We can use BM25 instead if we want
    searcher.setSimilarity(BM25Similarity()) # set BM25 as the scoring model
    
    # Define a parser for queries, set to parse the 'body' field
    parser = QueryParser('body', StandardAnalyzer())
    parsed_query = parser.parse(query)
    
    # Perform the search and retrieve the top 10 hits
    top_docs = searcher.search(parsed_query, 10).scoreDocs
    top_k_docs = [{} for i in range(10)]

    # Print each hit (document)
    # Printing here is just for testing
    # The web-based interface will probably need to retrieve top_docs and display the docs on the interface
    for i, hit in enumerate(top_docs):
        doc = searcher.doc(hit.doc)
        top_k_docs[i]["score"] = hit.score
        top_k_docs[i]["title"] = doc.get("title")
        top_k_docs[i]["body"] = doc.get("body").replace('\n', '<br>')
        top_k_docs[i]["url"] = doc.get("url")
        top_k_docs[i]["permalink"] = doc.get("permalink")
        top_k_docs[i]["created_utc"] = doc.get("created_utc")
    return top_k_docs

# Assuming reddit data is in 'reddit_data' directory and index will be created in 'reddit_index' directory
create_index('reddit_data', 'reddit_index')
#The query is being written here mannually, but we'll need to get the user inserted query from the web based interface
retrieve('reddit_index', 'your search query')

#for item in retrieve('reddit_index', 'stock'):
    #print(item['title'], item['score'])
