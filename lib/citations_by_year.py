import networkx as nx
import matplotlib.pyplot as plt

# a is a 1-7 digit number, with zeroes in front removed
# 1123 => 0001123 which year 2000, month 01, paper #123
def to_year(a):
  unparsed = ("%07d" % a)
  prefix = "19"
  if unparsed[0] == "0":
    prefix = "20"
  return int(prefix + unparsed[0:2])
  
print to_year(1234)

G = nx.DiGraph()

f = open("../data/cit-HepTh.txt")

for l in f:
  sp = l.split()
  n1, n2 = int(sp[0]), int(sp[1])
  if to_year(n1) == to_year(n2) == 1995:
    G.add_edge(n1,n2)

nx.draw(G)
plt.savefig("citations_1995.png")

# G = nx.read_edgelist("cit-HepTh.txt", delimiter=" ", nodetype=int, create_using=nx.DiGraph())
# # print G.nodes()
# 
# nx.draw(G)
# plt.savefig("citations_overall.png")