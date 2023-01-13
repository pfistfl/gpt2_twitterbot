# GPT-2 Twitter Bot

This repository contains code for training and deploying a twitter bot.
Made with [Pytorch](https://pytorch.org/), [Huggingface](https://huggingface.co/) and a pretrained german GPT-2 model from [Bayrische Staatsbibliothek](https://github.com/dbmdz).
In this instance, we train a bot for the german language.


The bot can be set up as follows:

**Structure:**
1. Download a training dataset from twitter 
2. Train a GPT-2 model
3. Deploy the bot

## Example: A.I.王er

To provide an example, we create a twitter bot for a german politician: Hubsi AI王er

### 0. Setup

* Clone or download this repository, it contains the necessary code to develop the bot.
* Navigate to the folder and install* the required Python modules using `pip -r install requirements.txt`.
* To download tweets and post tweets, you need a **Twitter Developer Account**. 
    After obtaining a Twitter developer account and setting up the bot account, we obtain the API keys and secret that allows us to get and post using the Twitter API.
    We add the API keys to a file `.env` that is loaded by the script to authenticate with the twitter API.
    The repository contains an empty `.env` file that can be filled out.


### 1. Data Download

Tweets can either be obtained via the official Twitter API or crawled from the web.
The `src/get_tweets.py` file contains the information on the `TWITTER_USER_ID` that needs to be adapted to the specific twitter user.
Now running `scripts/download.sh` should download available tweets and replies (up to a maximum of 3200, limited by the Twitter API).
The downloaded tweets can be found in the `data` folder.


### 2. Model training

As a base model, we use the GPT-2 model trained on german text from Huggingface.
Such a model was e.g. made available by the **Bayrisches Staatsbibliothek** on Huggingface via [huggingface/dbmdz](https://huggingface.co/dbmdz). We simply use the training script made available by Huggingface [here](https://github.com/huggingface/transformers/tree/main/examples/pytorch) to train our model.

To train the model, simply run `scripts/train.sh`. Note, this requires installed Pytorch with CUDA support and an available GPU.

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
In order to deploy the bot via docker, you can use the included Dockerfile.
Simply run `docker build -t <TAG> .` and then `docker run <TAG>` to run the bot.

### Roadmap

A lot of improvements can still be made to extend the existing bot. 
For now, tweets are often cut off at 144 characters and this might often result in unfinished tweets.
Furthermore, some tweets do not make a lot of sense (just like a politicitian's tweets :), but we could try to get better by improving the model and hyperparameters of the tweet generation.
