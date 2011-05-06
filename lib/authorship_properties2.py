import os
import glob
import re
import networkx as nx
import itertools
import matplotlib.pyplot as plt
import pickle
from collections import defaultdict
from PlotFunctions import *

# Read in Authorship Graph
clustering_coefficients = {}
connected_components = {}
diameters = {}
avg_shortestpath = {}
avg_degrees = {}
degrees = {}
avg_collablength = {}
collablength = {}
for year in range(1992, 2003):
  print "For year %d..." % year
  G = nx.read_edgelist("../data/parsed/authorship_%d.edgelist" % year, create_using=nx.Graph(), comments='#', delimiter='|', data=True, encoding='utf-8')
  
  print "\tCalculating and Plotting Degree Distribution..."
  degrees[year] = nx.degree(G)
  plot_frequency_distribution("degree_distribution_%d" % year, degrees[year], xlabel='Degree', ylabel='Number of Authors', linetype='o')
  
  print "\tCalculating Average Clustering Coefficient..."
  clustering_coefficients[year] = nx.average_clustering(G)
  
  print "\tCalculating Proportion in Largest Connected Component"
  largest_cc_graph = nx.connected_component_subgraphs(G)[0]
  connected_components[year] = float(len(largest_cc_graph)) / float(len(G))
  
  print "\tCalculating Diameter of Largest Connected Component..."
  diameters[year] = nx.diameter(largest_cc_graph)
  
  print "\tCalculating Average Shortest Path Length of Largest Connected Component"
  avg_shortestpath[year] = nx.average_shortest_path_length(largest_cc_graph)
  
  print "\tCalculating Average Degree..."
  avg_degrees[year] = float(sum(degrees[year].values())) / len(degrees[year])
  
  print "\tCalculating and Plotting Length of Collaboration Distribution"
  lengths = defaultdict(int)
  for _,_,eattr in G.edges_iter(data=True):
    length = max(eattr['years']) - min(eattr['years']) + 1
    lengths[length] += 1
  collablength[year] = lengths
  plot_xy("collab_length_distribution_%d" % year, collablength[year], ylabel='Number of Collaborations', xlabel='Length of Collaboration', log=True)
  
  print "\tCalculating Average Length of Collaboration"
  total = 0
  for years,count in lengths.iteritems():
    total += years * count
  avg_collablength[year] = float(total) / G.number_of_edges()

# Plotting More Graphs...

print "Plotting Average Clustering Coefficient..."
plot_xy("avg_clustering_coefficient", clustering_coefficients, ylabel='Average Clustering Coefficient')

print "Plotting Largest Connected Component..."
plot_xy("largest_cc", connected_components, ylabel='Proportion in Largest Connected Component')

print "Plotting Diameter..."
plot_xy("diameter", diameters, ylabel='Diameter of Largest Connected Component')

print "Plotting Average Degree..."
plot_xy("average_degree", avg_degrees, ylabel='Average Degree')

print "Plotting Average Shortest Path Length..."
plot_xy("average_shortestpath", avg_shortestpath, ylabel='Avg Shortest Path in Largest Connected Component')

print "Plotting Average Collab Length..."
plot_xy("average_collablength", avg_collablength, ylabel='Average Length of Collaboration')

# Saving data
print "Saving data..."
data = {}
data['clustering_coefficients'] = clustering_coefficients
data['connected_components'] = connected_components
data['diameters'] = diameters
data['avg_shortestpath'] = avg_shortestpath
data['average_degrees'] = avg_degrees
data['degrees'] = degrees
data['collablength'] = collablength
data['average_collablength'] = avg_collablength
with open("../data/graph_data.dat","w") as f:
  pickle.dump(data,f)