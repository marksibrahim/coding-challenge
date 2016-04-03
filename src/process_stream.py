"""
process incoming tweets in tweets.txt
returning the hashtag and timestamp of each
"""
import json, os

in_path = os.path.join( os.path.dirname( __file__ ), "..", 
        "tweet_input/tweets.txt")

class Tweets():
    """
    processes incoming tweets for hashtags and timestamps
    """
    def __init__(self, path=in_path):
        self.tweets_path = path

    def extract_hashtags(self, tweet_dict):
        """
        returns hashtags in a tweet as a set
        """
        hashtags = []
        for hashtag in tweet_dict["entities"]["hashtags"]:
            hashtags.append(hashtag["text"])
        return set(hashtags)

    
    def stream(self):
        """
        returns an iterable of
        (time_stamp, hashtags) for each tweet
        hashtags are a set
        """
        with open(self.tweets_path, 'r') as f:
            for tweet in f:
                try:
                    tweet_dict = json.loads(tweet)
                except ValueError:
                    #skip lines that can't be json decoded
                    continue

                try:
                    #skip if tweets contains 1 or fewer hashtags
                    if len(tweet_dict["entities"]["hashtags"]) < 2:
                        continue
                    hashtags = self.extract_hashtags(tweet_dict)
                    timestamp = tweet_dict["created_at"]
                    yield (timestamp, hashtags)
                except KeyError:
                    #skip lines in data not containg tweets
                        # like rate limit lines mentioned in challenge
                    continue

            



