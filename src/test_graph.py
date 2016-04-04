"""
test average degree of hashtag graph generated
"""

from itertools import islice

import os
import pandas as pd
import process_stream
import graph_degree

# Test how data is streamed from input.txt

in_path = "/Users/mark/Desktop/mark/repos/insight_data/coding-challenge/tweet_input/test_tweets.txt"
out_path = "/Users/mark/Desktop/mark/repos/insight_data/coding-challenge/tweet_output/output.txt"

tweets = process_stream.Tweets(in_path)
graph = graph_degree.Graph(in_path, out_path)


def test_stream():
    #test only first 5 tweets
    for values in islice(tweets.stream(), 5):
        timestamp, hashtags = values
        #does timestamp contain at least one digit?
        assert any(s.isdigit() for s in timestamp)

        #does hashtag set contain 2 or more elements?
        assert len(hashtags) > 1


# Test graph generation 

sample_hashtags = set(["A", "B", "C", "D"])

def test_set_to_edges():
    edges = graph.set_to_edges(sample_hashtags)
    #contains "A" <--> "B" 
    assert set(["A", "B"]) in edges
    assert set(["A", "D"]) in edges
    assert set(["B", "D"]) in edges
    #length of edge set should be two 
    assert len(edges[0]) == 2

    # number of edges
    assert len(edges) == 6

def test_first_edges():
    values = graph.get_first_edges()
    times = values[0]
    edges = values[1]
    #test time type
    assert type(times[0]) == pd.tslib.Timestamp
    #test presence of a hashtag
    assert isinstance(list(edges[0])[0], str)
    assert any(s.isalpha() for s in list(edges[0])[0])

def test_df_initialization():
    assert graph.df.shape[0] > 0 
