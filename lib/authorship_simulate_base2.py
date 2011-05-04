import os
import glob
import re
import networkx as nx
import itertools
import matplotlib.pyplot as plt
import pickle
from collections import defaultdict
from PlotFunctions import *
import random
from scipy.stats import gamma
import math

# Variables that can be modified
START_YEAR = 1997 # Year to start simulation from (i.e. start simulation from START_YEAR+1)
NEW_EDGES_PER_YEAR = 1350 # Number of new edges per year
T = 6 # Years to simulate
P = 0.0 # Probability of choosing a neighbor
Q = 0.0 # Probability of choosing at random or closing a triangle, etc.
PREFIX = "base2"

# Simulate from START_YEAR
G = nx.read_edgelist("authorship_%d.edgelist" % START_YEAR, create_using=nx.Graph(), comments='#', delimiter='|', data=True, encoding='utf-8')

def num_new_nodes(year, author):
  # Constant Activity Level
  if random.random() < 0.663:
    return 1
  else:
    return 0

for t in range(START_YEAR+1,START_YEAR+1+T):
  print "Simulating year %d..." % t
  
  # Generate bins for preferential attachment
  bins = []
  for node,degree in G.degree_iter():
    bins += [node] * degree
  
  # Create new edges for existing nodes
  print "\t for existing nodes"
  # Sum product of degrees
  print "\t\t Calculating Cumulative Sum..."
  nd_dict = G.degree()
  cumulative_sum = 0.0
  for node,degree in G.degree_iter():
    nd_dict.pop(node)
    for d2 in nd_dict.itervalues():
      cumulative_sum += degree * d2
  
  print "\t\t Iterating Over All Possible Edges"    
  nd_dict = G.degree()
  for node,degree in G.degree_iter():
    nd_dict.pop(node)
    for n2, d2 in nd_dict.iteritems():
      p = degree * d2 * 2 * 0.663 / cumulative_sum 
      if random.random() < p:
        if G.has_edge(node,n2):
          G[node][n2]['weight'] += 1
          G[node][n2]['years'].append(t)
        elif node != n2:
          G.add_edge(node, n2, weight=1, years=[t])
    
  # New node additions
  print "\t for new nodes"
  if len(G.nodes()) > 0:
    # Generate bins for preferential attachment
    bins = []
    for node,degree in G.degree_iter():
      bins += [node] * degree
      
    # Add new nodes and connect them to existing nodes using preferential attachment
    for i in range(0,NEW_EDGES_PER_YEAR):
      new_node = "N"+str(t)+"_"+str(i)
      # Pick & connect to a random node
      G.add_edge(random.choice(bins), new_node, weight=1, years=[t])
  
  nx.write_edgelist(G, "../data/simulations/%ssim_%d_%d_%f_%f.edgelist" % (PREFIX, START_YEAR, t, P, Q), comments='#', delimiter='|', data=True, encoding='utf-8')
      
#print G.edges()

# # Uncomment the below to visualize the graph. Might take extremely long to render!
# nx.draw_graphviz(G)
# plt.show()