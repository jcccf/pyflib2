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
START_YEAR = 1999 # Start year
NEW_EDGES_PER_YEAR = 1350
T = 6 # Years to simulate
P = 0.3 # Probability of choosing a neighbor
Q = 0.3 # Probability of choosing at random or closing a triangle, etc.

# # Simulate from the single-edge graph
G = nx.Graph()
G.add_edge("1","2", weight=1, years=[START_YEAR])

# # Simulate from START_YEAR
# G = nx.read_edgelist("authorship_%d.edgelist" % START_YEAR, create_using=nx.Graph(), comments='#', delimiter='|', data=True, encoding='utf-8')

for t in range(START_YEAR+1,START_YEAR+1+T):
  
  # Create new edges for existing nodes
  for node in G.nodes_iter():
    for i in range(0, 10): # TODO Change this to reflect rate of edge formation of a node
      
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
    
  # Create new nodes and attach them at random (NOT pref attachment right now!)
  if len(G.nodes()) > 0:
    target_edges = []
    for i in range(0,NEW_EDGES_PER_YEAR):
      target_edges += [["N"+str(t)+"_"+str(i), random.choice(G.nodes())]]
    for target_node, new_node in target_edges:
      G.add_edge(target_node, new_node, weight=1, years=[t])
      
print G.edges()

# # Uncomment the below to visualize the graph. Might take extremely long to render!
# nx.draw_graphviz(G)
# plt.show()