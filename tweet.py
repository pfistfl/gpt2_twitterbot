import requests
from requests_oauthlib import OAuth1
import os
from generate import generate

from dotenv import load_dotenv
load_dotenv()

consumer_key = os.environ.get("CONSUMER_KEY")
consumer_secret = os.environ.get("CONSUMER_SECRET")
access_token = os.environ.get("ACCESS_TOKEN")
access_token_secret = os.environ.get("ACCESS_TOKEN_SECRET")

def format_tweet(gens):
  gens = [g for g in gens if sum([1 for x in g if x == "#"]) < 3]
  if (len(gens) == 0):
    return {}
  elif (len(gens) == 1):
    return {"text": gens[0]}
  else:
    # Return longest tweet
    return {"text": max(gens, key=len)}

def connect_to_oauth(consumer_key, consumer_secret, acccess_token, access_token_secret):
    url = "https://api.twitter.com/2/tweets"
    auth = OAuth1(consumer_key, consumer_secret, acccess_token, access_token_secret)
    return url, auth

if __name__ == "__main__":
  debug = True
  gens = generate()
  payload = format_tweet(gens)
  if len(gens) and not debug:
    print(payload)
    url, auth = connect_to_oauth(
      consumer_key, consumer_secret, access_token, access_token_secret
    )
    request = requests.post(
      auth=auth, url=url, json=payload, headers={"Content-Type": "application/json"}
    )
    print(f"Posted tweet: {payload}")
  else:
    print(payload)