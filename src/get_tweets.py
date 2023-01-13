import tweepy
import re
import random
import math
import torch
from dotenv import load_dotenv

# Adapt this to download tweets from a different twitter user.
TWITTER_USER_ID = 702495475275079680

# Adapted from
# https://github.com/borisdayma/huggingtweets/blob/master/dev/huggingtweets-dev.ipynb
def clean_tweet(tweet, allow_new_lines = False):
    bad_start = ['http:', 'https:']
    for w in bad_start:
        tweet = re.sub(f" {w}\\S+", "", tweet)      # removes white space before url
        tweet = re.sub(f"{w}\\S+ ", "", tweet)      # in case a tweet starts with a url
        tweet = re.sub(f"\n{w}\\S+ ", "", tweet)    # in case the url is on a new line
        tweet = re.sub(f"\n{w}\\S+", "", tweet)     # in case the url is alone on a new line
        tweet = re.sub(f"{w}\\S+", "", tweet)       # any other case?
    tweet = re.sub(' +', ' ', tweet)                # replace multiple spaces with one space (makes the previous work worthless?)
    if not allow_new_lines:                         
        tweet = ' '.join(tweet.split())
    
    tweet = re.sub(r"@\S+", "", tweet)              # User mentions
    
    tweet = tweet.replace('&', '&')                   # Replace special chars
    tweet = tweet.replace('<', '<')
    tweet = tweet.replace('>', '>')
    return tweet.strip()

def load_data(fp):
    with open(fp, "r") as f:
        lines = f.readlines()    
    return [l.strip() for l in lines]

def to_dataset(dataset, epochs=4):
    limit = '<|endoftext|>'                      # Tweet delimiter
    dataset = [t for t in dataset]
    fulltext = limit
    for _ in range(epochs):
        random.shuffle(dataset)
        fulltext += limit.join(dataset) + limit    
    return fulltext

    
def save_train_test(fp, fraction=0.9):
    fp1 = 'data/tweets_replies.txt'
    tweets = load_data(fp1)

    out = ""
    for t in talks:
        if len(out) + len(t) < 144:
            out += " " + t
        else:
            tweets += [out]
            out = ""        

    # split dataset
    train_size = math.ceil(fraction * len(tweets))
    valid_size = len(tweets) - train_size
    train_dataset, valid_dataset = torch.utils.data.random_split(tweets, [train_size, valid_size])
    
    with open('data/train.txt', 'w+') as f:
        f.write(to_dataset(train_dataset, epochs=4))

    with open('data/valid.txt', 'w+') as f:
        f.write(to_dataset(valid_dataset, epochs=1))        
    

min_id = 1e31
if __name__ == '__main__':
    
    load_dotenv()
    bearer_token = os.environ.get("BEARER_TOKEN")
    client = tweepy.Client(bearer_token)
    
    # Dump all tweets into a file "tweets_replies.txt"
    ids = []
    for response in tweepy.Paginator(client.get_users_tweets, TWITTER_USER_ID, exclude=['retweets'], max_results=100).flatten(limit=3200):
        text, tid = response.data.get('text'), response.data.get('id')
        text = clean_tweet(text)
        
        if len(text) > 36:
            with open('data/tweets_replies.txt','a+') as f:
                f.write(text+"\n")
            ids += [int(tid)]
    
    min_id = min(min_id, min(ids))
    print(f"Got {len(ids)} tweets.")
    print(f"Minimum ID: {min_id}")
    
    # Perform a train-test split and save into a train.txt and valid.txt
    save_train_test()
        