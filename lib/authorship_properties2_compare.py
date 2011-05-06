import os
import glob
import re
import networkx as nx
import itertools
import matplotlib.pyplot as plt
import pickle
from collections import defaultdict
from PlotFunctions import *

# START_YEAR = 1997
# T = 5 #6
# P = 0.4
# Q = 0.4
# PREFIX = "p"

def doComparison(START_YEAR=1997,T=5,P=0.4,Q=0.4,PREFIX="p"):

  path = "%s%d_%.2f_%.2f/" % (PREFIX,START_YEAR,P,Q)
  if not os.path.exists("../data/graphs/"+path):
    os.makedirs("../data/graphs/"+path)

  with open("../data/graph_data.dat","r") as f:
    base_data = pickle.load(f)

  default_labels = ['Predicted', 'Actual']
  default_yaxis = (0,1)

  clustering_coefficients = {}
  connected_components = {}
  diameters = {}
  avg_shortestpath = {}
  avg_degrees = {}
  avg_collablength = {}
  for year in range(START_YEAR+1,START_YEAR+1+T):
    print "For %d..." % year
    G = nx.read_edgelist("../data/simulations/%ssim_%d_%d_%f_%f.edgelist" % (PREFIX,START_YEAR, year, P, Q), create_using=nx.Graph(), comments='#', delimiter='|', data=True, encoding='utf-8')
  
    print "\tCalculating and Plotting Degree Distribution..."
    nd = nx.degree(G)
    plot_frequency_distribution_array(path+"degree_distribution_%d" % year, [nd,base_data['degrees'][year]], ylabel='Number of Authors', xlabel='Degree', labels=default_labels, linetype='o')
  
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
    avg_degrees[year] = float(sum(nd.values())) / len(nd)
  
    print "\tCalculating and Plotting Length of Collaboration Distribution"
    lengths = defaultdict(int)
    for _,_,eattr in G.edges_iter(data=True):
      length = max(eattr['years']) - min(eattr['years']) + 1
      lengths[length] += 1
    plot_xy_array(path+"collab_length_distribution_%d" % year, [lengths,base_data['collablength'][year]], labels=default_labels, ylabel='Number of Collaborations', xlabel='Length of Collaboration', log=True)
  
    print "\tCalculating Average Length of Collaboration"
    total = 0
    for years,count in lengths.iteritems():
      total += years * count
    avg_collablength[year] = float(total) / G.number_of_edges()

  # Plotting More Graphs...

  print "Plotting Average Clustering Coefficient..."
  plot_xy_array(path+"avg_clustering_coefficient", [clustering_coefficients,base_data['clustering_coefficients']], labels=default_labels, ylabel='Clustering Coefficient', mse=True, yaxis=default_yaxis)

  print "Plotting Largest Connected Component..."
  plot_xy_array(path+"largest_cc", [connected_components,base_data['connected_components']], labels=default_labels, ylabel='Proportion in Largest Connected Component', mse=True, yaxis=default_yaxis)

  print "Plotting Diameter..."
  plot_xy_array(path+"diameter", [diameters,base_data['diameters']])

  print "Plotting Average Shortest Path Length..."
  plot_xy_array(path+"average_shortestpath", [avg_shortestpath,base_data['avg_shortestpath']], labels=default_labels, ylabel='Avg Shortest Path in Largest Connected Component', mse=True)

  print "Plotting Average Degree..."
  plot_xy_array(path+"average_degree", [avg_degrees,base_data['average_degrees']], labels=default_labels, ylabel='Average Degree', mse=True, yaxis=(0,10))

  print "Plotting Average Collaboration Length..."
  plot_xy_array(path+"average_collablength", [avg_collablength,base_data['average_collablength']], labels=default_labels, ylabel='Average Length of Collaboration (Years)', mse=True, yaxis=(0,10))
  
doComparison(START_YEAR=1997,T=5,P=0.4,Q=0.4,PREFIX="")
doComparison(START_YEAR=1997,T=5,P=0.4,Q=0.4,PREFIX="p")
doComparison(START_YEAR=1997,T=5,P=0.4,Q=0.4,PREFIX="p38k2")
doComparison(START_YEAR=1997,T=5,P=0.4,Q=0.4,PREFIX="ca")
doComparison(START_YEAR=1997,T=5,P=0.4,Q=0.4,PREFIX="cb")
doComparison(START_YEAR=1997,T=5,P=0.4,Q=0.4,PREFIX="cc")
doComparison(START_YEAR=1997,T=5,P=0.4,Q=0.4,PREFIX="cd")
doComparison(START_YEAR=1997,T=5,P=0.0,Q=0.0,PREFIX="base")
doComparison(START_YEAR=1997,T=5,P=0.0,Q=0.0,PREFIX="base2")
doComparison(START_YEAR=1997,T=5,P=0.0,Q=0.0,PREFIX="base2b")