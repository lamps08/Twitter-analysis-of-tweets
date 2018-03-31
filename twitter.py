# -*- coding: utf-8 -*-
"""
Created on Sun Mar  4 15:49:40 2018
#To Collect tweets from twiiter
#Reference - Dr. Gene Moo Lee notes for Data Science
@author: lamps08
"""
from twython import TwythonStreamer
import json
import sys
tweets = []
class MyStreamer(TwythonStreamer):


    # overriding
    def on_success(self, data):
        if 'lang' in data and data['lang'] == 'en':
            
            tweets.append(data['text'])
            print ('tweet #', len(tweets), data['text'][:200])
            with open('twitter.json', 'w') as fp:
                json.dump(tweets, fp, sort_keys=True, indent=4)
           # print(data['text'].encode('utf-8'))
            if len(tweets)>10:
                self.disconnect()
    def on_error(self, status_code, data):
        print(status_code)
        self.disconnect()
 


with open('your_twitter_credentials.json', 'r') as f:
    credentials = json.load(f)

# create your own app to get consumer key and secret
CONSUMER_KEY = credentials['CONSUMER_KEY']
CONSUMER_SECRET = credentials['CONSUMER_SECRET']
ACCESS_TOKEN = credentials['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = credentials['ACCESS_TOKEN_SECRET']

while len(tweets)<=10:
   try:
       stream = MyStreamer(CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
       stream.statuses.filter(track='twitter')
   except :
       continue