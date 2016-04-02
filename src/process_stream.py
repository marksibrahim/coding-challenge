"""
process incoming tweets in tweets.txt
returning the hashtag and timestamp of each
"""
import json

class Tweets():
    """
    processes incoming tweets for hashtags and timestamps
    """
    def __init__(self, test_mode = False):
        if test_mode:
            path =  "../tweet_input/test_tweets.txt"
        else:
            path = "../tweet_input/tweets.txt"
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
                tweet_dict = json.loads(tweet)
                #skip if tweets contains 1 or fewer hashtags
                if len(tweet_dict["entities"]["hashtags"]) < 2:
                    continue
                hashtags = self.extract_hashtags(tweet_dict)
                timestamp = tweet_dict["created_at"]
                yield (timestamp, hashtags)
            



