import json
import logging
import getpass
import requests
from config import *
from sys import argv
from requests_oauthlib import OAuth1
from urlparse import parse_qs

class tweetMojo():
   twitter_user = None
   twitter_oauth = None
   
   def __init__(self):        
      oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=TWITTER_TOKEN, resource_owner_secret=TWITTER_TOKEN_SECRET)
      self.twitter_oauth = oauth
       
   def new_twitter_user(self, twitter_user):
       self.twitter_user = twitter_user

   def get_n_tweets(self, username, last_n_tweets=1):
       req = requests.get(url="https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=%s&count=%d" % (username, last_n_tweets), auth=self.twitter_oauth)
       return [tweet['text'] for tweet in req.json()]
   
   def parse_tweet_for_instamojo_offer(self, tweet):
       formdata = {}
       
   
if __name__ == '__main__':
    logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    try:
        username = argv[1]
    except IndexError:
        raise Exception("Please mention the username.")
    logging.info('username: %s' % username)
    my_mojo = tweetMojo()
    my_mojo.new_twitter_user(username)
    print my_mojo.get_n_tweets(username)
    
