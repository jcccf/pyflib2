import os
import glob
import re
import networkx as nx
import itertools
import matplotlib.pyplot as plt
import pickle
from collections import defaultdict

# Calculate total number of citations an author receives up to that year
for year in range(1992, 2004):
  author_numcitations = defaultdict(int)
  with open("../data/parsed/citations_%d.count" % year,"r") as f:
    papers_citations = pickle.load(f)
  with open("../data/parsed/author_papers_%d.dat" % year,"r") as f:
    author_papers = pickle.load(f)
    
  for author,papers in author_papers.iteritems():
    for paper in papers:
      author_numcitations[author] += papers_citations[paper]
    
  with open('../data/parsed/author_numcitations_%d.dat' % year, 'w') as f:
    pickle.dump(author_numcitations, f)