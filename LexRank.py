#!/usr/bin/python
import networkx as nx
import similarity
from nltk.tokenize import word_tokenize
import numpy as np
import miscellaneous as ms
import itertools
import argparse

#The graph is built using the similarity scores obtained from the idf_modified_cosine() method
#
def build_graph(nodes, threshold, idf):
    gr = nx.Graph() #initialize an undirected graph
    gr.add_nodes_from(nodes)
    nodePairs = list(itertools.combinations(nodes, 2))

    #add edges to the graph (weighted by cosine similarity)
    for pair in nodePairs:
        node1 = pair[0]
        node2 = pair[1]
        simval = similarity.idf_modified_cosine(word_tokenize(node1), word_tokenize(node2), idf)
        if simval > threshold:
            gr.add_edge(node1, node2, weight=simval)

    return gr

#would have used this method if not for nx.pagerank
'''
def get_Bij(gr):
    A = nx.adjacency_matrix(gr, None, weight='weight')
    A = A.toarray()
    B = []
    row_sum = np.sum(A, axis=1)
    it = 0
    for row in A:
        r = []
        for ele in row:
            r.append(ele/row_sum[it])
        it += 1
        B.append(r)
'''

#key sentences are obtained
def get_keysentences(graph):
    # weight is the similarity value obtained from the idf_modified_cosine
    calculated_page_rank = nx.pagerank(graph, weight='weight')
    #most important words in ascending order of importance
    keysentences = sorted(calculated_page_rank, key=calculated_page_rank.get, reverse=False)
    return keysentences

def get_top(data, topn, threshold):
    sent_tokens, word_tokens = ms.tokenize(data)
    words = list(set(ms.get_words(data)))
    N = len(sent_tokens)
    idf = similarity.idf(word_tokens, words, N)
    matrix = similarity.get_similarity_matrix(word_tokens, idf)
    gr = build_graph(sent_tokens, threshold, idf)
    keysentences = get_keysentences(gr)
    return keysentences[:topn]
    
if __name__ == "__main__":
    #creating a argparser
    parser = argparse.ArgumentParser(description="Pass the data fname and threshold value")
    parser.add_argument("fname", help="Provide the data file name")
    parser.add_argument("threshold", help="Provide the threshold value", default=0.15, type=float)
    parser.add_argument("N", help="Top N sentences to be picked", default=10, type=int)
    args = parser.parse_args()
    with open(args.fname, "r") as f:
        data = f.read()
    sent_tokens, word_tokens = ms.tokenize(data)
    words = list(set(ms.get_words(data)))
    N = len(sent_tokens)
    idf = similarity.idf(word_tokens, words, N)
    matrix = similarity.get_similarity_matrix(word_tokens, idf)
    print ("Printing similarity matrix:\n", matrix)
    gr = build_graph(sent_tokens, args.threshold, idf)
    keysentences = get_keysentences(gr)
    print ("Printing Top 10 Key sentences:\n",keysentences[:args.N])
