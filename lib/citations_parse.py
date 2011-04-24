import networkx as nx
import matplotlib.pyplot as plt
import pickle
from collections import defaultdict

# a is a 1-7 digit number, with zeroes in front removed
# 1123 => 0001123 which year 2000, month 01, paper #123
def to_year(a):
  unparsed = ("%07d" % a)
  prefix = "19"
  if unparsed[0] == "0":
    prefix = "20"
  return int(prefix + unparsed[0:2])

print to_year(1234)

#G = nx.DiGraph()

def make_inner():
  return defaultdict(int)

num_citations = defaultdict(int)
papers_cpapers = defaultdict(list)
papers_citations = defaultdict(make_inner)

for t in range(1992,2004):
  print "Parsing for year %d" % t
  with open("../data/cit-HepTh.txt") as f:
    for l in f:
      sp = l.split()
      n1, n2 = sp[0], sp[1]
      if to_year(int(n1)) <= t and to_year(int(n2)) <= t:
        num_citations[n2] += 1
        papers_cpapers[n1].append(n2)
        papers_citations[n2][to_year(int(n1))] += 1
        #G.add_edge(n1,n2)
    with open('../data/parsed/citations_%d.count' % t, 'w') as f:
      pickle.dump(num_citations, f)
    with open('../data/parsed/papers_cpapers_%d.dat' % t, 'w') as f:
      pickle.dump(papers_cpapers, f)
    with open('../data/parsed/papers_citations_%d.dat' % t, 'w') as f:
      pickle.dump(papers_citations, f)

# nx.draw(G)
# plt.savefig("citations_1995.png")

# G = nx.read_edgelist("cit-HepTh.txt", delimiter=" ", nodetype=int, create_using=nx.DiGraph())
# # print G.nodes()
# 
# nx.draw(G)
# plt.savefig("citations_overall.png")