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
G = nx.read_edgelist("authorship.edgelist", comments='#', delimiter='|', data=True, encoding='utf-8')

# More algorithms here
# http://networkx.lanl.gov/reference/algorithms.html

# # Get degree distribution
# plot_frequency_distribution("degree_distribution", nx.degree(G))

# # Get paper distribution
# with open("authorship.count", "r") as f:
#   num_papers = pickle.load(f)
# plot_frequency_distribution("papers_per_author", num_papers)

# Get activity levels
# Get the years of collaboration for each person. Sort by year.
authors = defaultdict(list)
for n, nbrs in G.adjacency_iter():
  for nbr, eattr in nbrs.items():
    authors[n] += eattr['years']
# Convert the years of collaboration into frequency counts
newauthors = {}
for author,years in authors.iteritems():
  dcount = [(a, years.count(a)) for a in set(years)] # Count frequency of each degree
  dcount = sorted(dcount, key=lambda x: x[0])
  dcount = [(year - dcount[0][0], ycount) for year, ycount in dcount]
  newauthors[author] = dcount

# # Plot number of new authors a year
# years_author = defaultdict(int)
# for author,years in authors.iteritems():
#   years_author[min(years)] += 1
# print years_author
# plt.clf()
# plt.title("Average is %d" % (sum(years_author.values(), 0.0) / len(years_author.values())))
# plt.plot(years_author.keys(), years_author.values(), 'k')
# plt.savefig("new_authors_per_year.png")

# Plot activity distribution
activities = defaultdict(int)
for _,years in authors.iteritems():
  if len(years) < 50:
    activities[len(years)] += 1
#plt.plot(, activities.values(), 'ro')
plt.clf()
plt.hist(activities.keys(), 50, weights=activities.values(), normed=False, facecolor='green', align='mid', alpha=0.75, log=True)
plt.savefig("../data/graphs/activity_distribution_log.png")
plt.clf()
plt.hist(activities.keys(), 50, weights=activities.values(), normed=False, facecolor='green', align='mid', alpha=0.75, log=False)
plt.savefig("../data/graphs/activity_distribution.png")

# # Calculate average activity level
# collaborations, active_years = 0, 0
# for _,years in authors.iteritems():
#   # Count # of active years
#   first_year = int(sorted(years)[0])
#   active_years += 2003 - first_year + 1
#   collaborations += len(years)
# print float(collaborations) / active_years

# # Plot average # of collaborations
# for x in [0, 1, 10, 20, 50, 100]:
#   plt.clf()
#   years_cumulative = defaultdict(int)
#   num_authors = 0
#   for author,years in newauthors.iteritems():
#     #print author
#     # years_t = zip(*years) # Transpose
#     # plt.plot(years_t[0], years_t[1], 'k') # Plot
#     if len(authors[author]) > x:
#       num_authors += 1
#       for year, count in years:
#         years_cumulative[year] += count
#   years, counts = years_cumulative.keys(), years_cumulative.values()
#   for i in range(0, len(counts)):
#     counts[i] = float(counts[i]) / float(num_authors)
#   plt.plot(years, counts, 'k')
#   plt.savefig("activity_level_%d.png" % x)

# # Plot average # of collaborations (non-cumulative)
# for x,x2 in [[0,10], [10,20], [20,30], [30,40], [40,50], [50,60], [60,100], [100,1000]]:
#   plt.clf()
#   years_cumulative = defaultdict(int)
#   num_authors = 0
#   for author,years in newauthors.iteritems():
#     #print author
#     # years_t = zip(*years) # Transpose
#     # plt.plot(years_t[0], years_t[1], 'k') # Plot
#     if (len(authors[author]) > x) and (len(authors[author]) <= x2):
#       num_authors += 1
#       for year, count in years:
#         years_cumulative[year] += count
#   years, counts = years_cumulative.keys(), years_cumulative.values()
#   for i in range(0, len(counts)):
#     counts[i] = float(counts[i]) / float(num_authors)
#   plt.title("%d < x <= %d / %d authors" % (x,x2,num_authors))  
#   plt.plot(years, counts, 'k')
#   plt.savefig("../data/graphs/s_activity_level_%d.png" % x)
  
# # Plot general graph
# plt.clf()
# for author,years in newauthors.iteritems():
#   years_t = zip(*years) # Transpose
#   plt.plot(years_t[0], years_t[1], 'k') # Plot
# plt.savefig("activity_level_all.png" % x)
  
# # Iterating through edges
# for n,nbrs in G.adjacency_iter():
#   for nbr,eattr in nbrs.items():
#     print eattr['years']

# # Things you can print out
# print G.nodes()
# print G.edges()
# print nx.betweenness_centrality(G)
# print nx.degree(G)
# print nx.number_connected_components(G)