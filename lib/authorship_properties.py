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
T = 5 #6
P = 0.0
Q = 0.0
PREFIX = "base"
year = 2002 #2003

path = "%s%d_%.2f_%.2f/" % (PREFIX,START_YEAR,P,Q)
if not os.path.exists("../data/graphs/"+path):
  os.makedirs("../data/graphs/"+path)

# Read in Authorship Graph
#G = nx.read_edgelist("authorship.edgelist", comments='#', delimiter='|', data=True, encoding='utf-8')
G = nx.read_edgelist("../data/simulations/%ssim_%d_%d_%f_%f.edgelist" % (PREFIX,START_YEAR, year, P, Q), create_using=nx.Graph(), comments='#', delimiter='|', data=True, encoding='utf-8')

# Get activity levels
# Get the years of collaboration for each person. Sort by year.
def get_activity_levels(G):
  authors = defaultdict(list)
  for n, nbrs in G.adjacency_iter():
    for nbr, eattr in nbrs.items():
      authors[n] += eattr['years'] #[elem for elem in eattr['years'] if elem != 2003]
  # Convert the years of collaboration into frequency counts
  newauthors = {}
  for author,years in authors.iteritems():
    dcount = [(a, years.count(a)) for a in set(years)] # Count frequency of each degree
    dcount = sorted(dcount, key=lambda x: x[0])
    dcount = [(year - dcount[0][0], ycount) for year, ycount in dcount]
    newauthors[author] = dcount
  return authors, newauthors

# # Get degree distribution
# plot_frequency_distribution("degree_distribution", nx.degree(G))

# # Get paper distribution
# with open("authorship.count", "r") as f:
#   num_papers = pickle.load(f)
# plot_frequency_distribution("papers_per_author", num_papers)

authors, newauthors = get_activity_levels(G)

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
plt.savefig("../data/graphs/%sactivity_distribution_log.png" % path)
plt.clf()
plt.hist(activities.keys(), 50, weights=activities.values(), normed=False, facecolor='green', align='mid', alpha=0.75, log=False)
plt.savefig("../data/graphs/%sactivity_distribution.png" % path)

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

# Plot average # of collaborations (non-cumulative)
plt.clf()
alevels = {}
#for x,x2 in [[0,10], [10,20], [20,30], [30,40], [40,50], [50,60], [60,100], [100,1000]]:
for x,x2 in [[0,10], [10,20], [20,30], [30,40], [40,50], [50,60], [60,10000]]:
  years_cumulative = defaultdict(int)
  num_authors = 0
  for author,years in newauthors.iteritems():
    #print author
    # years_t = zip(*years) # Transpose
    # plt.plot(years_t[0], years_t[1], 'k') # Plot
    if (len(authors[author]) > x) and (len(authors[author]) <= x2):
      num_authors += 1
      for year, count in years:
        years_cumulative[year] += count
  years, counts = years_cumulative.keys(), years_cumulative.values()
  for i in range(0, len(counts)):
    counts[i] = float(counts[i]) / float(num_authors)
  alevels[(x,x2)] = dict(zip(years,counts))
  #plt.title("%d < x <= %d / %d authors" % (x,x2,num_authors))  
  plt.plot(years, counts, '-', label=r'$%d < x \leq %d$' % (x,x2))

alevels2 = {}
G2 = nx.read_edgelist("authorship_2002.edgelist", comments='#', delimiter='|', data=True, encoding='utf-8')
authors, newauthors = get_activity_levels(G2)
for x,x2 in [[0,10], [10,20], [20,30], [30,40], [40,50], [50,60], [60,10000]]:
  years_cumulative = defaultdict(int)
  num_authors = 0
  for author,years in newauthors.iteritems():
    #print author
    # years_t = zip(*years) # Transpose
    # plt.plot(years_t[0], years_t[1], 'k') # Plot
    if (len(authors[author]) > x) and (len(authors[author]) <= x2):
      num_authors += 1
      for year, count in years:
        years_cumulative[year] += count
  years, counts = years_cumulative.keys(), years_cumulative.values()
  for i in range(0, len(counts)):
    counts[i] = float(counts[i]) / float(num_authors)
  alevels2[(x,x2)] = dict(zip(years,counts))
  #plt.title("%d < x <= %d / %d authors" % (x,x2,num_authors))  
  plt.plot(years, counts, '--', label=r'$%d < x \leq %d$' % (x,x2))

texty, mse_total = "", 0.0  
for key in sorted(alevels):
  dict1 = alevels[key]
  dict2 = alevels2[key]
  combined = dict((k, [dict1.get(k), dict2.get(k)]) for k in set(dict1.keys() + dict2.keys()))
  print combined
  mse = 0.0
  for v,v2 in combined.itervalues():
    mse += (v-v2)**2
  mse /= len(combined)
  mse_total += mse
  texty += "%s : %f\n" % (str(key), mse)
texty += "Total : %f" % mse_total
  
leg = plt.legend(loc='best')
for t in leg.get_texts():
    t.set_fontsize('small')    # the legend text fontsize
leg.get_frame().set_alpha(0.4)
plt.figtext(0.14,0.67,texty).set_fontsize('small')
plt.savefig("../data/graphs/%ss_activity_level_all.png" % path)


# # Plot maturity time
# maturities = defaultdict(int)
# def to_year(unparsed):
#   prefix = "19"
#   if unparsed[0] == "0":
#     prefix = "20"
#   return int(prefix + unparsed[0:2])
# with open("../data/parsed/citations_2002.count","r") as f:
#   papers_citations = pickle.load(f)
# G = nx.read_edgelist("../data/parsed/authorship_2002.edgelist", comments='#', delimiter='|', data=True, encoding='utf-8')
# for _,_,eattr in G.edges_iter(data=True):
#   firstYear = sorted(eattr['years'])[0]
#   maxPaper, maxCitations = "", -1
#   for paper in eattr['papers']:
#     #print paper, papers_citations[paper]
#     if papers_citations[paper] > maxCitations:
#       maxCitations = papers_citations[paper]
#       maxPaper = paper
#   #print "Max is"
#   #print maxPaper
#   #print maxCitations
#   if maxCitations > 0:
#     maturityTime = to_year(maxPaper) - firstYear
#     maturities[maturityTime] += 1
# plot_xy("maturity_time", maturities)

# Get paper-citations hash
# For each edge, find the time from the first paper to the paper with the highest citations
# 
  
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