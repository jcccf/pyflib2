#
# Generates co-authorship graph from abstract files
# The co-authorship graph ignores papers written by a single person
# Expects abstracts to be located at ../data/cit-HepTh-abstracts/
# Also prints out # of papers written per author
#

import os
import glob
import re
import networkx as nx
import itertools
import matplotlib.pyplot as plt
import pickle
from collections import defaultdict

# Converts a filename into the corresponding year.
# e.g. "0012999" becomes 2000
def file_to_year(a):
  unparsed = (a.rsplit("/",1)[1]).split(".")[0]
  prefix = "19"
  if unparsed[0] == "0":
    prefix = "20"
  return int(prefix + unparsed[0:2])

G = nx.Graph()
num_papers = defaultdict(int)

# Build authorship graph for 1992-2003
# Nodes are author names
# Edges have edge weights G[a1][a2]['weight'] (an integer)
# and the years in which authors collaborated G[a1][a2]['years'] (a list)
for year in range(1992, 2004):
  print "Reading in authorship graph for %d" % year
  path = '../data/cit-HepTh-abstracts/%d/' % year
  for infile in glob.glob( os.path.join(path, '*.abs') ):
    #print "current file is: " + infile
    f = open(infile)
    #print file_to_year(infile)
    for l in f:
      if re.match("Authors:", l):
        sp = l.split(":")
        authors = map(lambda s: s.strip(), re.split(r',| and ', sp[1])) # Separate by commas and "and", and strip whitespace
        authors = [elem for elem in authors if elem != ""] # Filter out empty strings
        
        # Count papers for each author
        for author in authors:
          num_papers[author] += 1
        
        if len(authors) > 1: # Ignore papers with a single author
          for a1, a2 in itertools.combinations(authors, 2): # Pick all possible pairs of authors of a paper
            a1, a2 = [a2,a1] if a1 > a2 else [a1,a2] # Order each pair in alphabetical order
            #print "%s %s" % (a1,a2)
            if (a1,a2) in G.edges():
              G[a1][a2]['weight'] += 1
              G[a1][a2]['years'].append(file_to_year(infile))
            else:
              G.add_edge(a1, a2, weight=1, years=[file_to_year(infile)])
  nx.write_edgelist(G, "authorship_%d.edgelist" % year, comments='#', delimiter='|', data=True, encoding='utf-8')

# Write Graph to File
nx.write_edgelist(G, "authorship.edgelist", comments='#', delimiter='|', data=True, encoding='utf-8')

# Write Authorship Counts to File
with open('authorship.count', 'w') as f:
  pickle.dump(num_papers, f)