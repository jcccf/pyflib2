import networkx as nx
import matplotlib.pyplot as plt
import pickle
from collections import defaultdict
from PlotFunctions import *

def make_inner():
  return defaultdict(int)

with open('../data/parsed/citations_2003.count', 'r') as f:
  num_citations = pickle.load(f)

with open("../data/parsed/papers_citations_2003.dat", "r") as f:
  papers_citations = pickle.load(f)

# Output citation distribution
citation_dist = defaultdict(int)
for times in num_citations.values():
  if times <= 1000:
    citation_dist[times] += 1  
plt.clf()
plt.xlabel("Number of citations")
plt.ylabel("Number of papers")
plt.loglog(citation_dist.keys(), citation_dist.values(),"o")
#plt.hist(citation_dist.keys(), 1000, weights=citation_dist.values(), normed=False, facecolor='green', align='mid', alpha=0.75, log=False)
plt.savefig("../data/graphs/citation_distribution.png")

# Print out average number of citations per paper
#print float(sum(num_citations.values())) / len(num_citations.keys())

papers_citations_normalized = {}
for paper, years in papers_citations.iteritems():
  y0 = sorted(years)[0]
  years = [((year - y0), ycount) for year, ycount in years.iteritems()]
  papers_citations_normalized[paper] = years
  
for x,x2 in [[0,10],[10,20],[30,40],[40,50],[50,60],[60,70],[70,80],[80,90],[90,100],[100,200],[200,300],[300,400],[400,500],[500,1000]]:
  plt.clf()
  years_cum, num_papers = defaultdict(int), 0
  for paper, years in papers_citations_normalized.iteritems():
    if num_citations[paper] > x and num_citations[paper] <= x2:
      num_papers += 1
      for year, count in years:
        years_cum[year] += count
  years, counts = years_cum.keys(), years_cum.values()
  counts = [float(c)/num_papers for c in counts]
  plt.title("%d < x <= %d citations / %d papers" % (x,x2,num_papers))  
  plt.plot(years, counts, 'k')
  plt.savefig("../data/graphs/s_citation_level_%d.png" % x)
  
# Number of citations against number of papers
with open("../data/parsed/author_papers_2002.dat","r") as f:
  author_papers = pickle.load(f)
with open("../data/parsed/author_numcitations_2002.dat", "r") as f:
  author_numcitations = pickle.load(f)
pn = [[len(author_papers[p]),author_numcitations[p]] for p in author_papers.keys()]
pn = zip(*pn)
plt.clf()
plt.xlabel("Number of papers")
plt.ylabel("Number of citations")
plt.plot(pn[0], pn[1], "o")
plt.savefig("../data/graphs/papers_to_citations.png")

G = nx.read_edgelist("../data/parsed/authorship_2002.edgelist", comments='#', delimiter='|', data=True, encoding='utf-8')
ncitations, ncollaborations = [], []
for author in author_papers.iterkeys():
  wd = G.degree(author,weighted=True)
  if type(wd) is not dict:
    ncitations.append(author_numcitations[author])
    ncollaborations.append(wd)
plt.clf()
plt.xlabel("Number of collaborations")
plt.ylabel("Number of citations")
plt.plot(ncollaborations, ncitations, "o")
plt.savefig("../data/graphs/collaborations_to_citations.png")