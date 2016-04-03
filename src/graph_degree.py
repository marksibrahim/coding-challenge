"""
outputs the average degree of the hashtag graph
based on input tweets generated by process_stream.py
"""
from itertools import islice

import process_stream
import pandas as pd
import sys, os

class Graph():
    """
    maintains hashtag graph for a 60-second sliding window
    contains average_degree method 
    """

    def __init__(self, in_path, out_path):
        """
        initializes tweet stream
        """
        self.tweets_stream =  process_stream.Tweets(in_path).stream()
        #dataframe containing edges within 60-second window
            # initialize with first set of hashtags
        first_edges = self.get_first_edges()
        self.df = pd.DataFrame({"time": first_edges[0], "node1": first_edges[1],
                "node2": first_edges[2]}).set_index("time")
        #initial timewindow
        self.min_time = self.df.index.max() - pd.Timedelta("60 sec")


        self.out_path = out_path

    def edges_to_nodes(self, edges):
        """
        converts edges into a two nodes lists: nodes1, nodes2
        """
        nodes1 = []
        nodes2 = []
        for edge in edges:
            edge_list = list(edge)
            node1 = edge_list[0]
            nodes1.append(node1)
            node2 = edge_list[1]
            nodes2.append(node2)
        return nodes1, nodes2

    def set_to_edges(self, hashtags):
        """
        converts a set of hashtags into edges
        edges are returned as sets inside a list
        """    
        edges = []
        for h in hashtags:
            for remaining_h in hashtags.difference(h):
                #frozenset creates an immutable set
                edge = set((h, remaining_h))
                if edge not in edges and len(edge) > 1:
                    edges.append(edge)
        return edges

    def get_first_edges(self):
        """
        returns the first [ [time], [node1 list], [node2 list]] from tweet stream
        """
        times = []

        for timestamp, hashtags in islice(self.tweets_stream, 1):
            edges = self.set_to_edges(hashtags)
            nodes1, nodes2 = self.edges_to_nodes(edges)
        #add timestamp
        for edge in edges:
            times.append(pd.Timestamp(timestamp))
        return [times, nodes1, nodes2]
            
    def add_hashtags(self, time, hashtags):     
        """
        appends hashtags to df
        and sets new min_time
        """
        edges = self.set_to_edges(hashtags)
        nodes1, nodes2 = self.edges_to_nodes(edges)
        times = [time for n in nodes1]
        df_to_add = pd.DataFrame({"time": times, "node1": nodes1, "node2": nodes2}).set_index("time")

        #append
        self.df = self.df.append(df_to_add)
        #update min time
        self.min_time = self.df.index.max() - pd.Timedelta("60 sec")
        #filter
        self.df = self.df[self.df.index > self.min_time]

    def average_degree(self):
        """
        computes the average degree in the graph
        """
        total_degree = self.df.shape[0]*2
        number_nodes = len(self.df["node1"].append(self.df["node2"]).unique())

        average_degree = float(total_degree) / float(number_nodes)
        return average_degree

    def write_degree_to_output(self, avg_degree):
        """
        write degree with two decimal precision to output
        """
        degree_str = '{:.2f}'.format(round(avg_degree, 2))
        with open(self.out_path, "a") as f:
            f.write(degree_str + "\n")

    def run(self):
        """
        runs streaming computation
        """
        #clear output file
        open(self.out_path, 'w').close()
        #write first average degree
        self.write_degree_to_output(self.average_degree())

        #stream tweets; skip first entry (processed during instantiation)
            # generator state is no on second element 
        for timestamp, hashtags in self.tweets_stream:
            time = pd.Timestamp(timestamp)
            if time > self.min_time:
                self.add_hashtags(time, hashtags)
                self.write_degree_to_output(self.average_degree())
            

if __name__ == "__main__":
    #in_path = sys.argv[0]
    #out_path = sys.argv[1]
    in_path = os.path.join( os.path.dirname( __file__ ), "..", 
            "tweet_input/tweets.txt")
    out_path = os.path.join( os.path.dirname( __file__ ), "..", 
            "tweet_output/output.txt")
    g = Graph(in_path, out_path)
    g.run()

