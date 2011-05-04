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
P = 0.4 # Probability of choosing a neighbor
Q = 0.4 # Probability of choosing at random or closing a triangle, etc.
PREFIX = "cc"

# # Simulate from the single-edge graph
# G = nx.Graph()
# G.add_edge("1","2", weight=1, years=[START_YEAR])

# Simulate from START_YEAR
G = nx.read_edgelist("../data/parsed/authorship_%d.edgelist" % START_YEAR, create_using=nx.Graph(), comments='#', delimiter='|', data=True, encoding='utf-8')

# Load year of first publication for each author
with open("authorship.year", "r") as f:
  first_paper = pickle.load(f)

# Load # of papers each author produces in his/her lifetime
with open("authorship.count", "r") as f:
  num_papers = pickle.load(f)

# Load paper => authors
with open("../data/parsed/paper_authors_2003.dat") as f:
  papers_authors = pickle.load(f)
  
# Load paper => cited papers
with open("../data/parsed/papers_cpapers_2003.dat") as f:
  papers_cpapers = pickle.load(f)

def num_new_nodes(year, author):
  # Constant Activity Level
  if random.random() < 0.663:
    return 1
  else:
    return 0

def num_papers_dist():
  return 4
  
def num_citations_dist():
  return 71

new_num_citations = {}
for t in range(START_YEAR+1,START_YEAR+1+T):
  print "Simulating year %d..." % t
  
  # Load # of citations
  with open("../data/parsed/citations_%d.count" % t) as f:
    num_citations = pickle.load(f)
  num_citations.update(new_num_citations)
  
  # Load authors => papers
  with open("../data/parsed/author_papers_%d.dat" % t) as f:
    authors_papers = pickle.load(f)

  
  # Create new edges for existing nodes
  print "\t for existing nodes"
  for node in G.nodes_iter():
    for i in range(0, num_new_nodes(t,node)):
      
      # See if we want to form an edge and set target if we want to
      rand = random.random()
      target = None
      if rand < P:
        # Pick an author out of those of papers which you cite in your papers
        # proportional to the number of papers they wrote
        bins = []
        cited_authors = {}
        for paper in authors_papers[node]:
          #print paper
          for cpaper in papers_cpapers[paper]:
            #print "\t"+cpaper
            for auth in papers_authors[cpaper]:
              #print "\t\t"+auth
              cited_authors[auth] = 1
        for auth in cited_authors.keys():
          bins += [auth] * len(authors_papers[auth])
        
        # Do preferential attachment if no existing authors cited (wow, really?)
        if len(bins) == 0:
          for node,degree in G.degree_iter():
            bins += [node] * degree
            
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
        #print "Adding edge from %s to %s" % (node,target)
        new_paper = "N"+str(t)+"_"+node+"_"+target
        num_citations[new_paper] = num_citations_dist()
        if G.has_edge(node,target):
          G[node][target]['weight'] += 1
          G[node][target]['years'].append(t)
          G[node][target]['papers'].append(new_paper)
        elif node != target:
          G.add_edge(node, target, weight=1, years=[t], papers=[new_paper])
    
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
      new_paper = "N"+str(t)+"_"+new_node
      new_num_citations[new_paper] = num_citations_dist()
      first_paper[new_node] = t
      num_papers[new_node] = num_papers_dist()
      # Pick & connect to a random node
      G.add_edge(random.choice(bins), new_node, weight=1, years=[t], papers=[new_paper])
  
  nx.write_edgelist(G, "../data/simulations/%ssim_%d_%d_%f_%f.edgelist" % (PREFIX, START_YEAR, t, P, Q), comments='#', delimiter='|', data=True, encoding='utf-8')
      
#print G.edges()

# # Uncomment the below to visualize the graph. Might take extremely long to render!
# nx.draw_graphviz(G)
# plt.show()