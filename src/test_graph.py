"""
test average degree of hashtag graph generated
"""
import process_stream
from itertools import islice
# Test how data is streamed from input.txt

tweets = process_stream.Tweets(test_mode = True)


def test_stream():
    #test only first 5 tweets
    for values in islice(tweets.stream(), 5):
        timestamp, hashtags = values
        #does timestamp contain at least one digit?
        assert any(s.isdigit() for s in timestamp)

        #does hashtag set contain 2 or more elements?
        assert len(hashtags) > 2



    
