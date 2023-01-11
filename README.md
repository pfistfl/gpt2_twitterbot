# GPT-2 Twitter Bot

This repository contains code for training and deploying a twitter bot.
In this instance, we train a bot for the german language.

The bot can be set up as follows:

**Structure:**
1. Download a training dataset from twitter 
2. Train a GPT-2 model
3. Deploy the bot

## Example: A.I.王er

To provide an example, we create a twitter bot for a german politician: Hubsi AI王er

### 1. Data Download

Tweets can either be obtained via the official Twitter API or crawled from the web.

### 2. Model training

As a base model, we use the GPT-2 model trained on german text from Huggingface.

### 3. Deployment

We mainly follow this [guide](https://developer.twitter.com/en/docs/tutorials/how-to-create-a-twitter-bot-with-twitter-api-v2) by twitter to set up a bot.
After obtaining a Twitter developer account and setting up the bot account, we obtain the API keys and secret that allows us to post using the Twitter API.
We add the API keys to a file `.env` that is loaded by the script to authenticate with the twitter API.
Once this is set up, run the following steps to set up the API:

    * Modify `src/generate.py`, providing the path to the trained model. Other settings can be adopted in the `Args` dataclass.
    * Set the debug Flag to `True` in `src/tweet.py`.
    * Run `scripts/tweet.sh` and inspect generated tweets, adapt `Args` for generation of tweets.
    * Once the tweets are satisfying, set  debug to `False`.
    * Automate the submission of tweets, e.g. via a `cron` job or a AWS Lambda / Azure function.

### Dockerfile
In order to deploy the Bo