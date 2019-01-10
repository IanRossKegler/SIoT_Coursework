from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import datetime
import sys
import time
import json

import twitter_credentials
from save_data import save_error, write_data, backup_data
from get_weather import get_weather
from counter import increment_counter, read_counter, reset_counter


# # # # TWITTER AUTHENTICATOR # # # #
class TwitterAuthenticator():
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


# # # # TWITTER STREAMER # # # #
class TwitterStreamer():
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        self.twitter_authenticator = TwitterAuthenticator()
        self.stream = None

    def stream_tweets(self, hash_tag_list):
        listener = TwitterListener()
        auth = self.twitter_authenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)
        self.stream = stream

        stream.filter(track=hash_tag_list, is_async=True)

    def disconnect(self):
        self.stream.disconnect()


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):

    def on_data(self, data):

        try:
            tweet = json.loads(data)
            search_terms = ['ldn', 'london', 'Ldn', 'London']

            if tweet['place'] is not None:
                for i in search_terms:
                    if tweet['place']['full_name'].find(i) != -1:
                        increment_counter()
                        return True

            elif tweet['user']['location'] is not None:
                for i in search_terms:
                    if tweet['user']['location'].find(i) != -1:
                        increment_counter()
                        return True

            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            save_error()
            sys.exit()


if __name__ == '__main__':
    hash_tag_list = ["depression", "mental health", "depressed", "anxiety", "anxious", "stress",
                     "mental health awareness", "ptsd", "mental health matters"]

    twitter_streamer = TwitterStreamer()

    increment = 2
    cycles = 0

    while True:
        twitter_streamer.stream_tweets(hash_tag_list)

        start = datetime.datetime.now()
        start += datetime.timedelta(minutes=increment/2)
        start -= datetime.timedelta(minutes=start.minute % increment, seconds=start.second, microseconds=start.microsecond)

        time.sleep(increment*60)

        weather = get_weather()

        count = read_counter()
        reset_counter()

        write_data(str(start), count, weather[0], weather[1])

        twitter_streamer.disconnect()

        cycles += 1

        if cycles >= 5:
            backup_data(str(datetime.datetime.now()))
            cycles = 0
