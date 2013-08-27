import json
import logging
import getpass
import requests
from config import *
import re
from sys import argv, exit
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
       offer_key_value = dict(re.findall(r'(\S+)=(".*?"|\S+)', tweet[1:]))
       return offer_key_value
       
   def check_tweet_is_instamoffer(self, tweet):
       return tweet.lower().startswith("instamoffer")
       
   def check_offer_parameters(self, offer_key_value):
       return "title" in offer_key_value and "desc" in offer_key_value and "file" in offer_key_value and ("usd" in offer_key_value or "inr" in offer_key_value)
   
if __name__ == '__main__':
    logging.basicConfig(filename='debug.log', level=logging.DEBUG)
    try:
        username = argv[1]
    except IndexError:
        raise Exception("Please mention the username.")
    logging.info('username: %s' % username)
    my_mojo = tweetMojo()
    my_mojo.new_twitter_user(username)
    latest_tweet = my_mojo.get_n_tweets(username)[0]
    if my_mojo.check_tweet_is_instamoffer(latest_tweet):
        offer_details = my_mojo.parse_tweet_for_instamojo_offer(latest_tweet)
        if my_mojo.check_offer_parameters(offer_details):
            print offer_details
        else:
            print "The tweet format does not match the specified format."
            exit()
    else:
        print "The tweet is not about an instamojo offer."
        exit()
        
    
