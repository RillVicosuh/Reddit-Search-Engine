# Reddit-Search-Engine

This project is composed of two main parts: Reddit post crawling/collecting and an indexing/search system. The collector system utilizes the PRAW Python library to crawl and gather data from specified subreddits. The search system, deployed on the UCR server, is a Flask-based web application that uses pylucene to index and search the collected Reddit posts.

## DEMO VIDEO: 
https://youtu.be/a-o47FwY8mI

## Part 1: Reddit Post Collector

### Architecture
The system uses the PRAW Python library to interact with Reddit’s API. It includes a collector script, a crawler script, and a seed file with subreddit names. The gathered Reddit post data, along with the metadata and comments, are stored in JSON files in a specified directory.

### Crawling Strategy 
The crawler uses the PRAW package to navigate Reddit's API, reading subreddit posts from the seed file and collecting various attributes. It prioritizes top posts and also examines newer ones. Crawling continues until a specified file size limit is met.

### Data Structures
The system uses encapsulated objects to represent each Reddit post, enhancing efficiency during data collection and storage.

### Limitations
The system's main limitation is the extensive time required for data collection due to the large volume of data and the rate limits imposed by Reddit's API.

### How to Run

#### Windows:

1. Ensure your project directory has the files: `reddit_Collector.py`, `crawler.bat`, and `seed.txt`.
   
2. The `crawler.bat` file should contain the following content:

    ```
    @echo off
    python reddit_Collector.py %*
    ```

3. The `seed.txt` file should contain the list of subreddits (one per line).
   
4. Open a Command Prompt or PowerShell window and navigate to the project directory.
   
5. Run the BAT file with the command (The second argument is the amount of reddit posts to collect from each subreddit):

    In Command Prompt:

    ```
    crawler.bat seed.txt 1000 output_directory
    ```

    In PowerShell:

    ```
    .\crawler.bat seed.txt 1000 output_directory
    ```

6. A new directory will be created, if it does not already exist, where the JSON files including the reddit post data will be stored.

#### Unix/Linux:

1. Ensure your project directory has the files: `reddit_Collector.py`, `crawler.sh`, and `seed.txt`.
   
2. The `crawler.sh` file should contain the following content:

    ```
    #!/bin/bash
    python3 reddit_crawler.py "$@"
    ```

3. The `seed.txt` file should contain the list of subreddits (one per line).
   
4. Open a terminal window and navigate to the project directory.
   
5. Make the script executable with the command:

    ```
    chmod +x crawler.sh
    ```

6. Run the script with the command:

    ```
    ./crawler.sh seed.txt 1000 output_directory
    ```

These instructions will set up the system to collect Reddit posts from specified subreddits and store the data in JSON files in the designated output directory.


## Part 2: Search System

### Architecture
The search system uses Lucene to create an index of Reddit data and perform search operations. It generates an index containing various attributes of each Reddit post, and also defines a function to handle search retrieval. The retrieved results are displayed on a Flask-based web interface.

### Index Structures
The system uses Lucene's native index structures including inverted index, posting lists, and document store. It employs the standard analyzer for tokenization, lowercasing, stopword removal, and stemming.

### Search Algorithm
The system parses user queries and searches through the body of the Reddit posts using the parsed queries. The BM25 sorting algorithm is used to rank the search results.

### Limitations
The system requires a stable internet connection and may take considerable time for tasks such as data parsing due to the BM25 algorithm and text indexing processes.

### Web Framework
The web backend uses Python and libraries like pylucene and Flask. The frontend of the web application is built with HTML and Flask. It consists of two templates: one for user query input and one for displaying the top 10 search results.

### How to Run

#### Prerequisites:

1. You need to have Flask installed as it is the web application framework used. If not already installed, you can do so by running `pip install flask` in your terminal.

#### Instructions for Indexing:

1. Navigate to your project directory. 

2. Run the following command to index all the Reddit posts in the JSON file located in the `reddit_data` folder:

    ```
    python3 pylucene.py
    ```

3. After indexing, the created index will be located in the `reddit_index` folder.

#### Instructions for Running the Web Application:

1. Make sure you are connected to the UCR VPN.

2. In your project directory, type the following command:

    ```
    flask run -h 0.0.0.0 -p 8888
    ```

3. The output of the command will be a URL. Open this URL in a web browser to access the web application.

4. On the web application, you can insert your query. The top 10 posts relevant to your query will be displayed in decreasing order of score.

By following these steps, you will be able to run the web application, which allows for querying the indexed Reddit posts.

## Overall Project Limitations and Improvements
The current system does have a few limitations, notably the dependency on a stable internet connection and the potentially long runtime due to data parsing, indexing, and BM25 algorithm processes. In the future, the system could be optimized by utilizing multithreading or distributed systems to speed up data collection and processing. Additionally, error handling could be improved to better manage potential network failures or API rate limits.

