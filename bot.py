# Modules
import tweepy
from dotenv import load_dotenv
import os
from time import sleep

def get_last_seen_id():
  text_file = open('last_seen_id.txt', 'r')
  last_seen_id = int(text_file.read().strip())
  text_file.close()
  return last_seen_id


def set_last_seen_id(last_seen_id_str):
  text_file = open('last_seen_id.txt', 'w')
  text_file.write(last_seen_id_str)
  text_file.close()
  return


def response(api):
  # retrieve last seen id
  last_seen_id = get_last_seen_id()

  # get all the mentions after the last seen tweet
  mentions_list = api.mentions_timeline(last_seen_id, tweet_mode='extended')

  # loop through all mentions (oldest first)
  for mention in reversed(mentions_list):

    # get the tweet id for current new tweet
    last_seen_id = mention.id

    # store this new id in text file for next iteration
    set_last_seen_id(mention.id_str)

    # get the tweet id of the base tweet
    base_tweet_id = mention.in_reply_to_status_id

    # get the base tweet using the base_tweet_id
    base_tweet = api.get_status(base_tweet_id)

    # get the video link
    video_link = base_tweet._json['entities']['media'][0]['expanded_url']


def main():
  # Load all environment variables from the .env file
  load_dotenv()

  # Store all API keys in variables
  CONSUMER_KEY = os.getenv('CONSUMER_KEY')
  CONSUMER_SECRET = os.getenv('CONSUMER_SECRET')
  ACCESS_KEY = os.getenv('ACCESS_KEY')
  ACCESS_SECRET = os.getenv('ACCESS_SECRET')

  # Authorization to consumer key and consumer secret 
  auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

  # Access to user's access key and access secret 
  auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

  # Calling api 
  api = tweepy.API(auth)

  # Keep running and refresh every 30 seconds
  while True:
    response(api)
    sleep(30)
    

if __name__ == '__main__':
  main()
