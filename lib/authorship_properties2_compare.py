import os
import glob
import re
import networkx as nx
import itertools
import matplotlib.pyplot as plt
import pickle
from collections import defaultdict
from PlotFunctions import *

START_YEAR = 1997
T = 6
P = 0.5
Q = 0.5

with open("../data/graph_data.dat","r") as f:
  base_data = pickle.load(f)

clustering_coefficients = {}
connected_components = {}
diameters = {}
avg_degrees = {}
for year in range(START_YEAR+1,START_YEAR+1+T):
  print "For %d..." % year
  G = nx.read_edgelist("../data/simulations/sim_%d_%d_%f_%f.edgelist" % (START_YEAR, year, P, Q), create_using=nx.Graph(), comments='#', delimiter='|', data=True, encoding='utf-8')
  
  print "\tCalculating and Plotting Degree Distribution..."
  #plot_frequency_distribution("degree_distribution_%d" % year, nx.degree(G))
  
  print "\tCalculating Average Clustering Coefficient..."
  clustering_coefficients[year] = nx.average_clustering(G)
  
  print "\tCalculating Proportion in Largest Connected Component"
  largest_cc_graph = nx.connected_component_subgraphs(G)[0]
  connected_components[year] = float(len(largest_cc_graph)) / float(len(G))
  
  print "\tCalculating Diameter of Largest Connected Component..."
  diameters[year] = nx.diameter(largest_cc_graph)
  
  print "\tCalculating Average Degree..."
  degree_sum = 0
  for node, degree in G.degree_iter():
    degree_sum += degree
  avg_degrees[year] = float(degree_sum) / float(len(G))

# Plotting More Graphs...

path = "%d_%.2f_%.2f/" % (START_YEAR,P,Q)
if not os.path.exists("../data/graphs/"+path):
  os.makedirs("../data/graphs/"+path)

print "Plotting Average Clustering Coefficient..."
plot_xy_array(path+"avg_clustering_coefficient", [clustering_coefficients,base_data['clustering_coefficients']])

print "Plotting Largest Connected Component..."
plot_xy_array(path+"largest_cc", [connected_components,base_data['connected_components']])

print "Plotting Diameter..."
plot_xy_array(path+"diameter", [diameters,base_data['diameters']])

print "Plotting Average Degree..."
plot_xy_array(path+"average_degree", [avg_degrees,base_data['average_degrees']])