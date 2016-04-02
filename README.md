Coding Challenge
===========================================================

Computes the average degree in a Twitter hastag graph based on an incoming stream of tweets. 

* degree of a hashtag * is the number of edges connected to the hashtag
* average degree * sum of the degree of each hashtag divided by the total number of hashtags

# Details
Tweets arrive as new lines in tweets.txt in tweet_input.
The average degree is computed as the average degree of a 60-second window 
(based on latest tweet)---the average degree is output to output.txt every time a new tweet
arrives (meaning a new line in tweets.txt is processed).


## Required Packages

Python 3.5

In addition itertools and the json modules from the standard library are used---no additional installation or setup is required.
