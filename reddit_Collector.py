import sys 
import praw
import json
import os
import requests
from bs4 import BeautifulSoup
import concurrent.futures

# Initialize PRAW with your credentials
reddit = praw.Reddit(client_id='cSdxizd5ZZsAorKw7pkeaw',
                     client_secret='oRtsPCo0m_Vy4Ae5EDbMSAdWxVuLbQ',
                     user_agent='python:CS172_Search_Engine4:v1.0 (by /u/RicoV7)',
                     username='',
                     password='')

# Get input parameters from command line
seed_file = sys.argv[1]
limit = int(sys.argv[2])
output_dir = sys.argv[3]

# Read subreddits from seed file
# Subreddits in seed file need to be one per line
with open(seed_file, 'r') as f:
    subreddits = [line.strip() for line in f.readlines()]

# Function to get HTML page title
def get_page_title(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup.title.string
    except:
        return None

#Retrieves the comments for each reddit post   
def get_comments(submission):
    try:
        #limitst the amount of comments loaded for processing per post 
        submission.comments.replace_more(limit=50)
        comments = []

        for comment in submission.comments.list():
            comments.append({
                'id': comment.id,
                'author': comment.author.name if comment.author else '',
                'created_utc': comment.created_utc,
                'body': comment.body,
                'score': comment.score,
            })

        return comments
    
    except Exception as e:
        print(f"An error occurred when getting comments: {e}")
        return []

# Function to collect and save Reddit posts
def collect_and_save_posts(subreddit_name):
    try:
        print(f"Processing subreddit: {subreddit_name}")
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        subreddit = reddit.subreddit(subreddit_name)
        output_file = os.path.join(output_dir, f"{subreddit_name}.jsonl")
        file_size = 0
        post_count = 0

        with open(output_file, 'w') as f:
            for submission in subreddit.top(limit=limit):
                #Retrieves the stated attributes of each reddit post
                post_data = {
                    'id': submission.id,
                    'title': submission.title,
                    'author': submission.author.name if submission.author else '',
                    'created_utc': submission.created_utc,
                    'score': submission.score,
                    'url': submission.url,
                    'permalink': submission.permalink,
                    'num_comments': submission.num_comments,
                    'selftext': submission.selftext,
                    'comments': get_comments(submission)
                }

                # Checks if post contains URL to an HTML page and get its title
                if submission.url and submission.url.startswith('http'):
                    title = get_page_title(submission.url)
                    if title:
                        post_data['external_title'] = title

                #Writes the reddit post data to the output file. One post per line.
                f.write(json.dumps(post_data) + "\n")
                file_size += len(json.dumps(post_data))
                post_count += 1 #Add to the total number of posts processed for a subreddit

                if file_size >= 10 * (1024 ** 2):  # 10 MB Limit 
                    break
            
            for submission in subreddit.new(limit=limit):
                #Retrieves the stated attributes of each reddit post
                post_data = {
                    'id': submission.id,
                    'title': submission.title,
                    'author': submission.author.name if submission.author else '',
                    'created_utc': submission.created_utc,
                    'score': submission.score,
                    'url': submission.url,
                    'permalink': submission.permalink,
                    'num_comments': submission.num_comments,
                    'selftext': submission.selftext,
                    'comments': get_comments(submission)
                }

                # Checks if post contains URL to an HTML page and get its title
                if submission.url and submission.url.startswith('http'):
                    title = get_page_title(submission.url)
                    if title:
                        post_data['external_title'] = title

                #Writes the reddit post data to the output file. One post per line.
                f.write(json.dumps(post_data) + "\n")
                file_size += len(json.dumps(post_data))
                post_count += 1 #Add to the total number of posts processed for a subreddit

                if file_size >= 10 * (1024 ** 2):
                    break  # 10 MB Limit 
        print(f"Finished processing posts for subreddit: {subreddit_name}")
        print(f"Number of posts retrieved: {post_count}")

    except Exception as e:
        print(f"An error occurred when processing subreddit {subreddit_name}: {e}")

def main():
    #Using concurrent.futures library for multithreading
    #running the collect_and_save_posts() function in parallel for multiple subreddits.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(collect_and_save_posts, subreddits)

    print("Finished processing all subreddits")

if __name__ == "__main__":
    main()