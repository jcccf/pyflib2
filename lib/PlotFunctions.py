import matplotlib.pyplot as plt

# name is the name of the PNG file you wish to save
# dict is a dictionary of key => value pairs, and you want to calculate the frequency
# distribution of ONLY the values
# E.g. {"hi" => 1, "bye" => 1, "abc" => 2} gives you values [1, 2] with frequency [2, 1]
def plot_frequency_distribution(name, dict):
  dlist = dict.values()
  dcount = [(a, dlist.count(a)) for a in set(dlist)] # Count frequency of each degree
  dcount = sorted(dcount, key=lambda x: -x[1]) # Sort by frequency descending
  dcount_t = zip(*dcount) # Transpose
  print dcount_t
  plt.clf()
  plt.plot(dcount_t[0], dcount_t[1], 'ro', dcount_t[0], dcount_t[1], 'k') # Plot
  plt.savefig("../data/graphs/%s.png" % name)
  
def plot_xy(name, dicty):
  plt.clf()
  plt.plot(dicty.keys(), dicty.values(), 'k')
  plt.savefig("../data/graphs/%s.png" % name)
  
def plot_xy_array(name, adicty):
  plt.clf()
  for dicty in adicty:
    plt.plot(dicty.keys(), dicty.values(), '-')
  plt.savefig("../data/graphs/%s.png" % name)