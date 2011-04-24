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

# Variables that can be modified
START_YEAR = 1999 # Year to start simulation from (i.e. start simulation from START_YEAR+1)
NEW_EDGES_PER_YEAR = 1350 # Number of new edges per year
T = 6 # Years to simulate
P = 0.3 # Probability of choosing a neighbor
Q = 0.3 # Probability of choosing at random or closing a triangle, etc.

# # Simulate from the single-edge graph
G = nx.Graph()
G.add_edge("1","2", weight=1, years=[START_YEAR])

# # Simulate from START_YEAR
# G = nx.read_edgelist("authorship_%d.edgelist" % START_YEAR, create_using=nx.Graph(), comments='#', delimiter='|', data=True, encoding='utf-8')

# Load year of first publication for each author
with open("authorship.year", "r") as f:
  first_paper = pickle.load(f)
# Load # of papers each author produces in his/her lifetime
with open("authorship.count", "r") as f:
  num_papers = pickle.load(f)

# TODO Should correctly decide how many papers an author "produces" each year
# based on num_papers, the # of papers he/she generates in his/her lifetime and
# the author's "age"
def num_new_nodes(year, author):
  npapers = num_papers[author]
  if npapers < 5:
    return 0
  fpaper = first_paper[author]
  return int(year - fpaper)
  
# TODO Should sample from the distribution of papers as in authorship.count
def num_papers_dist():
  return 4

for t in range(START_YEAR+1,START_YEAR+1+T):
  print "Simulating year %d..." % t
  
  # Create new edges for existing nodes
  print "\t for existing nodes"
  for node in G.nodes_iter():
    for i in range(0, num_new_nodes(t,node)):
      
      # See if we want to form an edge and set target if we want to
      rand = random.random()
      target = None
      if rand < P:
        # Pick a node proportional to edge weight
        bins = []
        for nbr in G.neighbors(node):
          bins += [nbr] * G[node][nbr]['weight']
        target = random.choice(bins)
      elif rand < P + Q:
        # Degree-random
        bins = []
        for nbr in G.neighbors(node):
          for nbr2 in G.neighbors(nbr):
            bins += [nbr2]
        target = random.choice(bins)
    
      # Form an edge if target is set, don't form self-loops
      if target:
        if G.has_edge(node,target):
          G[node][target]['weight'] += 1
          G[node][target]['years'].append(t)
        elif node != target:
          G.add_edge(node, target, weight=1, years=[t])
    
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
      first_paper[new_node] = t
      num_papers[new_node] = num_papers_dist()
      # Pick & connect to a random node
      G.add_edge(random.choice(bins), new_node, weight=1, years=[t])
  
  nx.write_edgelist(G, "../data/simulations/sim_%d_%d_%f_%f.edgelist" % (START_YEAR, t, P, Q), comments='#', delimiter='|', data=True, encoding='utf-8')
      
#print G.edges()

# # Uncomment the below to visualize the graph. Might take extremely long to render!
# nx.draw_graphviz(G)
# plt.show()