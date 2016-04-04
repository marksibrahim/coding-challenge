Coding Challenge
===========================================================

Computes the average degree in a Twitter hastag graph based on an incoming stream of tweets. 

* __degree of a hashtag__ is the number of other hashtags appearing together in a tweet
* __average degree__ sum of the degree of each hashtag divided by the total number of hashtags

To run: 
./run.sh

This executes "graph_degree.py" in the "src" directory.

# Details
## Algorithm
1. Tweets arrive as new lines in "tweets.txt" in tweet_input.
2. The average degree is computed over a 60-second window, based on the latest tweet. 
3. The average degree is written on a new line to "output.txt" every time a new tweet
arrives.

## Implementation 
In "src" directory, "process_stream.py" processes the input tweets line-by-line using a generator. 

Then, hashtags are converted into edges and nodes and stored as sets in a pandas dataframe inside "graph_degree.py"
After each tweet, a new average degree is stored on a new line in "output.txt"

# Requirements

This program is written in Python 3.5 and requires:

* pandas (0.17.1)

Although tested with Python 3.5, the program should be backwards compatible with Python > 2.7. 

