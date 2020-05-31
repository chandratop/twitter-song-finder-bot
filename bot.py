# Modules
import tweepy, os, sys, requests
from dotenv import load_dotenv
from time import sleep
from acrcloud.recognizer import ACRCloudRecognizer

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

def save_video(video_link):
  req = requests.get(video_link, allow_redirects=True)
  video_file = open('video.mp4', 'wb')
  video_file.write(req.content)
  video_file.close()
  return

def video_song_finder():
  # API vars
  acr_config = {
    'host': os.getenv('ACR_HOST_NAME'),
    'access_key': os.getenv('ACR_ACCESS_KEY'),
    'access_secret': os.getenv('ACR_ACCESS_SECRET'),
    'timeout': 10
  }
  
  # ACR object
  acr = ACRCloudRecognizer(acr_config)

  # recognize, 0s offset from start
  result = eval(acr.recognize_by_file('video.mp4', 0))

  if result['status']['msg'] == 'Success':
    print("success")
    # Recognized the song
    metadata = result['metadata']

    # extract the metadata/details
    best_find = metadata['music'][0]
    title = best_find['title']
    
    artist = best_find['artists'][0]['name']
    # if more than artist then we need to append
    if len(best_find['artists']) > 1:
      for artist in range(1, len(best_find['artists'])):
        artists += ", " + artist['name']
    
    # plug YouTube link if exists
    # youtube = ""
    # if 'youtube' in best_find['external_metadata']:
    #   youtube = 'https://www.youtube.com/watch?v=' + best_find['external_metadata']['youtube']['vid']
    try:
      youtube = 'https://www.youtube.com/watch?v=' + best_find['external_metadata']['youtube']['vid']
    except:
      youtube = ""

    # create tweet
    tweet = f"Yay, we found it!\nTitle: {title}\n"
    if len(best_find['artists']) > 1:
      tweet += f"Artists: {artists}\n"
    else:
      tweet += f"Artist: {artist}\n"
    if youtube != "":
      tweet += f"Youtube: {youtube}"    
  
  else:
    print("Failure")
    # Failed to recognize
    tweet = "It seems that we can't recognize this :("

  # return tweet
  return tweet


def response(api):
  print("in response")
  # retrieve last seen id
  last_seen_id = get_last_seen_id()

  # get all the mentions after the last seen tweet
  mentions_list = api.mentions_timeline(last_seen_id, tweet_mode='extended')

  # loop through all mentions (oldest first)
  for mention in reversed(mentions_list):

    # get the tweet id for current new tweet
    last_seen_id = mention.id
    print("last seen id: ", last_seen_id)

    # store this new id in text file for next iteration
    set_last_seen_id(mention.id_str)

    # get the tweet id of the base tweet
    base_tweet_id = mention.in_reply_to_status_id

    # get the base tweet using the base_tweet_id
    base_tweet = api.get_status(base_tweet_id)

    # get the video link
    try:
      variants = base_tweet._json['extended_entities']['media'][0]['video_info']['variants']
      for index in range(len(variants)):
        if variants[index]['content_type'] == 'video/mp4':
          video_link = base_tweet._json['extended_entities']['media'][0]['video_info']['variants'][index]['url']
          break
      print(video_link)
    except:
      print("exception no video")
      tweet = f"@{mention.user.screen_name}, you sure there's a video here?"
      api.update_status(tweet, mention.id)
      continue

    # save the video for use
    save_video(video_link)

    # Perform song recognition
    tweet = video_song_finder()
    tweet = f"@{mention.user.screen_name} " + tweet

    # post tweet
    api.update_status(tweet, mention.id)


def main():
  # Load all environment variables from the .env file
  load_dotenv()

  # Store all API keys in variables
  TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY')
  TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET')
  TWITTER_ACCESS_KEY = os.getenv('TWITTER_ACCESS_KEY')
  TWITTER_ACCESS_SECRET = os.getenv('TWITTER_ACCESS_SECRET')

  # Authorization to consumer key and consumer secret 
  auth = tweepy.OAuthHandler(TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET)

  # Access to user's access key and access secret 
  auth.set_access_token(TWITTER_ACCESS_KEY, TWITTER_ACCESS_SECRET)

  # Calling api 
  api = tweepy.API(auth)

  # Keep running and refresh every 30 seconds
  while True:
    response(api)
    sleep(30)
    

if __name__ == '__main__':
  main()
