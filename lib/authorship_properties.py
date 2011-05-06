import os
import glob
import re
import networkx as nx
import itertools
import matplotlib.pyplot as plt
import pickle
from collections import defaultdict
from PlotFunctions import *

path="real/"

# Read in Authorship Graph
#G = nx.read_edgelist("authorship.edgelist", comments='#', delimiter='|', data=True, encoding='utf-8')
G = nx.read_edgelist("../data/parsed/authorship_2002.edgelist", comments='#', delimiter='|', data=True, encoding='utf-8')

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

authors, newauthors = get_activity_levels(G)

# Get degree distribution
plot_frequency_distribution(path+"degree_distribution", nx.degree(G), ylabel="Number of Authors", xlabel="Degree", linetype='o')

# Get paper distribution
with open("../data/parsed/authorship.count", "r") as f:
  num_papers = pickle.load(f)
plot_frequency_distribution(path+"papers_per_author", num_papers, ylabel='Number of Authors', xlabel='Number of Papers', linetype='o')

# Plot number of new authors a year
years_author = defaultdict(int)
for author,years in authors.iteritems():
  years_author[min(years)] += 1
print years_author
plt.clf()
plt.figtext(0.14,0.86,"Average is %d" % (sum(years_author.values(), 0.0) / len(years_author.values()))).set_fontsize('small')
plt.plot(years_author.keys(), years_author.values(), 'k')
plt.ylabel("Number of New Authors")
plt.savefig("../data/graphs/real/new_authors_per_year.png")

# Plot activity distribution
activities = defaultdict(int)
for _,years in authors.iteritems():
  if len(years) < 50:
    activities[len(years)] += 1
plot_xy(path+"activity_distribution_log", activities, ylabel='Number of Authors', xlabel='Number of Collaborations', log=True)

# Calculate average activity level
collaborations, active_years = 0, 0
for _,years in authors.iteritems():
  # Count # of active years
  first_year = int(sorted(years)[0])
  active_years += 2003 - first_year + 1
  collaborations += len(years)
print float(collaborations) / active_years

# Plot average # of collaborations (cumulative)
plt.clf()
alevels = {}
authors, newauthors = get_activity_levels(G)
#for x,x2 in [[0,10], [10,20], [20,30], [30,40], [40,50], [50,60], [60,100], [100,1000]]:
for x,x2 in [[0,10], [10,20], [20,30], [30,40], [40,50], [50,60], [60,70], [70,80], [80,90], [90,100], [100,10000]]:
  years_cumulative = defaultdict(int)
  num_authors = 0
  for author,years in newauthors.iteritems():
    #print author
    # years_t = zip(*years) # Transpose
    # plt.plot(years_t[0], years_t[1], 'k') # Plot
    if (len(authors[author]) > x):
      num_authors += 1
      for year, count in years:
        years_cumulative[year] += count
  years, counts = years_cumulative.keys(), years_cumulative.values()
  for i in range(0, len(counts)):
    counts[i] = float(counts[i]) / float(num_authors)
  alevels[(x,x2)] = dict(zip(years,counts))
  #plt.title("%d < x <= %d / %d authors" % (x,x2,num_authors))  
  plt.plot(years, counts, '-', label=r'$x > %d$' % x)
leg = plt.legend(loc='best')
for t in leg.get_texts():
    t.set_fontsize('small')    # the legend text fontsize
leg.get_frame().set_alpha(0.4)
plt.ylabel('Average number of papers')
plt.xlabel('Years since first published paper')
plt.savefig("../data/graphs/real/activity_level_all_cumulative.png")

# Plot average # of collaborations (non-cumulative)
plt.clf()
alevels = {}
authors, newauthors = get_activity_levels(G)
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
leg = plt.legend(loc='best')
for t in leg.get_texts():
    t.set_fontsize('small')    # the legend text fontsize
leg.get_frame().set_alpha(0.4)
plt.ylabel('Average number of papers')
plt.xlabel('Years since first published paper')
plt.savefig("../data/graphs/real/activity_level_all.png")

# Plot maturity time
maturities = defaultdict(int)
def to_year(unparsed):
  prefix = "19"
  if unparsed[0] == "0":
    prefix = "20"
  return int(prefix + unparsed[0:2])
with open("../data/parsed/citations_2002.count","r") as f:
  papers_citations = pickle.load(f)
G = nx.read_edgelist("../data/parsed/authorship_2002.edgelist", comments='#', delimiter='|', data=True, encoding='utf-8')
for _,_,eattr in G.edges_iter(data=True):
  firstYear = sorted(eattr['years'])[0]
  maxPaper, maxCitations = "", -1
  for paper in eattr['papers']:
    #print paper, papers_citations[paper]
    if papers_citations[paper] > maxCitations:
      maxCitations = papers_citations[paper]
      maxPaper = paper
  #print "Max is"
  #print maxPaper
  #print maxCitations
  if maxCitations > 0:
    maturityTime = to_year(maxPaper) - firstYear
    maturities[maturityTime] += 1
plot_xy(path+"maturity_time", maturities, ylabel="Number of Authors", xlabel="Years from first to most cited collaborative paper")

# Plot maturity time (ALL PAPERS)
print "Now Maturity Time All Papers"
author_maturity = defaultdict(list)
maturities = defaultdict(int)
with open("../data/parsed/citations_2002.count","r") as f:
  papers_citations = pickle.load(f)
with open("../data/parsed/author_papers_2002.dat","r") as f:
  author_papers = pickle.load(f)
with open("../data/parsed/author_numcitations_2002.dat", "r") as f:
  author_numcitations = pickle.load(f)
for author,papers in author_papers.iteritems():
  maxPaper, maxCitations, firstYear = "", -1, 9999
  for paper in papers:
    if firstYear > to_year(paper):
      firstYear = to_year(paper)
    if papers_citations[paper] > maxCitations:
      maxCitations = papers_citations[paper]
      maxPaper = paper
  if maxCitations > 0 and firstYear < 2004:
    maturityTime = to_year(maxPaper) - firstYear
    author_maturity[author] = [author_numcitations[author],maturityTime]
    #maturities[maturityTime] += 1
plt.clf()
for x,x2 in [[0,100], [100,200], [200,400], [400,600], [600,800], [800,1000], [1000,10000]]:
  maturities = defaultdict(int)
  for citations, maturityTime in author_maturity.itervalues():
    if citations > x and citations <= x2:
      maturities[maturityTime] += 1
  total_auth = sum(maturities.values())
  plt.plot(maturities.keys(), [float(m)/total_auth for m in maturities.values()], '-', label=r'$%d < x \leq %d$' % (x,x2))
leg = plt.legend(loc='best')
for t in leg.get_texts():
    t.set_fontsize('small')    # the legend text fontsize
leg.get_frame().set_alpha(0.4)
plt.ylabel('Proportion of Authors')
plt.xlabel('Years from first to most cited paper')
plt.savefig("../data/graphs/real/maturity_time_all.png")  

# Plot Num Papers against Num Authors
num_authors = defaultdict(int)
with open("../data/parsed/paper_authors_2002.dat","r") as f:
  paper_authors = pickle.load(f)
for authors in paper_authors.itervalues():
  num_authors[len(authors)] += 1
plot_xy(path+"authors_per_paper", num_authors, xlabel='Number of Coauthors', ylabel='Number of Papers')

# Plot Num Citations against Num Authors
cum_citations = defaultdict(float)
for paper,authors in paper_authors.iteritems():
  cum_citations[len(authors)] += papers_citations[paper]
for numa,count in num_authors.iteritems():
  cum_citations[numa] /= count
plot_xy(path+"citations_to_numauthors", cum_citations, xlabel='Number of Coauthors', ylabel='Average Number of Citations')

# Plot diff in highest cited and lowest cited author
# Num of citations is picked from the previous year. Ex. for a paper published in 1999, look at the # of citations received by
# authors only up to 1998, to discount the effect of citations toward that paper itself, and to look at existing "street cred"
# of the authors
# Num Citations
with open("../data/parsed/citations_2002.count","r") as f:
  papers_citations = pickle.load(f)
with open("../data/parsed/paper_authors_2002.dat","r") as f:
  paper_authors = pickle.load(f)
author_numcitations = {}
for i in range(1992,2002):
  with open("../data/parsed/author_numcitations_%d.dat" % i, "r") as f:
    author_numcitations[i] = pickle.load(f)
# For each paper, check if it has more than X citations
paperz,i = [],1
plt.clf()
for paper,citations in papers_citations.iteritems():
  paper_year = to_year(paper) - 1
  if citations > 1000 and paper_year >= 1992:
    print paper,citations
    minCitations, maxCitations = 999999, -1
    for author in paper_authors[paper]:
      print "\t"+author
      if author_numcitations[paper_year][author] < minCitations:
        minCitations = author_numcitations[paper_year][author]
      if author_numcitations[paper_year][author] > maxCitations:
        maxCitations = author_numcitations[paper_year][author]
    papr = {minCitations: i, maxCitations: i}
    i += 1
    plt.semilogy([i,i], [minCitations,maxCitations], '-', [i,i], [minCitations,maxCitations], 'ko', markersize=2.0, mew=0.0)
    paperz.append(papr)
print paperz
plt.gca().axes.get_xaxis().set_visible(False)
plt.ylabel("Number of Citations")
plt.title("Difference in citations received by coauthors in papers (> 1000 citations)")
plt.savefig("../data/graphs/real/paper_minmaxcitations.png")  
#plot_xy_array(path+"paper_minmaxcitations", paperz)
    

# # Iterating through edges
# for n,nbrs in G.adjacency_iter():
#   for nbr,eattr in nbrs.items():
#     print eattr['years']