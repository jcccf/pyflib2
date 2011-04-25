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
avg_degrees = {}
degrees = {}
for year in range(1992, 2004):
  G = nx.read_edgelist("authorship_%d.edgelist" % year, create_using=nx.Graph(), comments='#', delimiter='|', data=True, encoding='utf-8')
  
  print "Calculating and Plotting Degree Distribution..."
  degrees[year] = nx.degree(G)
  plot_frequency_distribution("degree_distribution_%d" % year, degrees[year])
  
  print "Calculating Average Clustering Coefficient..."
  clustering_coefficients[year] = nx.average_clustering(G)
  
  print "Calculating Proportion in Largest Connected Component"
  largest_cc_graph = nx.connected_component_subgraphs(G)[0]
  connected_components[year] = float(len(largest_cc_graph)) / float(len(G))
  
  print "Calculating Diameter of Largest Connected Component..."
  diameters[year] = nx.diameter(largest_cc_graph)
  
  print "Calculating Average Degree..."
  degree_sum = 0
  for node, degree in G.degree_iter():
    degree_sum += degree
  avg_degrees[year] = float(degree_sum) / float(len(G))

# Plotting More Graphs...

print "Plotting Average Clustering Coefficient..."
plot_xy("avg_clustering_coefficient", clustering_coefficients)

print "Plotting Largest Connected Component..."
plot_xy("largest_cc", connected_components)

print "Plotting Diameter..."
plot_xy("diameter", diameters)

print "Plotting Average Degree..."
plot_xy("average_degree", avg_degrees)

# Saving data
print "Saving data..."
data = {}
data['clustering_coefficients'] = clustering_coefficients
data['connected_components'] = connected_components
data['diameters'] = diameters
data['average_degrees'] = avg_degrees
data['degrees'] = degrees
with open("../data/graph_data.dat","w") as f:
  pickle.dump(data,f)