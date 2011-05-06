import matplotlib.pyplot as plt

# name is the name of the PNG file you wish to save
# dict is a dictionary of key => value pairs, and you want to calculate the frequency
# distribution of ONLY the values
# E.g. {"hi" => 1, "bye" => 1, "abc" => 2} gives you values [1, 2] with frequency [2, 1]
def plot_frequency_distribution(name, dict, xlabel='', ylabel='', title='', linetype='k'):
  if linetype == 'o':
    plt.rcParams['axes.color_cycle'] = ['#282F36', '#FFFEFC', '#BDA21D', '#BFBC5B', '#D2E098']
  else:
    plt.rcParams['axes.color_cycle'] = ['b','g','r','c','m','y','k']
  dlist = dict.values()
  dcount = [(a, dlist.count(a)) for a in set(dlist)] # Count frequency of each degree
  dcount = sorted(dcount, key=lambda x: x[0]) # Sort by number ascending -x[1] freq desc
  dcount_t = zip(*dcount) # Transpose
  print dcount_t
  plt.clf()
  if len(xlabel) > 0:
    plt.xlabel(xlabel)
  if len(ylabel) > 0:
    plt.ylabel(ylabel)
  if len(title) > 0:
    plt.title(title)
  plt.loglog(dcount_t[0], dcount_t[1], linetype) # Plot
  plt.savefig("../data/graphs/%s.png" % name)
  
def plot_frequency_distribution_array(name, adicty, labels=[], xlabel='', ylabel='', title='', linetype='-'):
  plt.clf()
  #plt.rcParams['axes.color_cycle'] = ['#1C2B33', '#B2182D', '#0E6638', '#D9561B', '#BFA51B']
  if linetype == 'o':
    plt.rcParams['axes.color_cycle'] = ['#282F36', '#FFFEFC', '#BDA21D', '#BFBC5B', '#D2E098']
  else:
    plt.rcParams['axes.color_cycle'] = ['b','g','r','c','m','y','k']
  if len(xlabel) > 0:
    plt.xlabel(xlabel)
  if len(ylabel) > 0:
    plt.ylabel(ylabel)
  if len(title) > 0:
    plt.title(title)

  for dicty,labely in map(None,adicty,labels):
    dlist = dicty.values()
    dcount = [(a, dlist.count(a)) for a in set(dlist)] # Count frequency of each degree
    dcount = sorted(dcount, key=lambda x: x[0]) # Sort by number ascending
    dcount_t = zip(*dcount) # Transpose
    #print dcount_t
    #plt.plot(dcount_t[0], dcount_t[1], '.', dcount_t[0], dcount_t[1], '-') # Plot
    if labely:
      plt.loglog(dcount_t[0], dcount_t[1], linetype, label=labely)
    else:
      plt.loglog(dcount_t[0], dcount_t[1], linetype)
  if len(labels) > 0:
    leg = plt.legend(loc='best')
    for t in leg.get_texts():
      t.set_fontsize('small')    # the legend text fontsize
  plt.savefig("../data/graphs/%s.png" % name)
  
def plot_xy(name, dicty, xlabel='', ylabel='', title='', log=False, linetype='k'):
  if linetype == 'o':
    plt.rcParams['axes.color_cycle'] = ['#282F36', '#FFFEFC', '#BDA21D', '#BFBC5B', '#D2E098']
  else:
    plt.rcParams['axes.color_cycle'] = ['b','g','r','c','m','y','k']
  plt.clf()
  if len(xlabel) > 0:
    plt.xlabel(xlabel)
  if len(ylabel) > 0:
    plt.ylabel(ylabel)
  if len(title) > 0:
    plt.title(title)
  if log:
    plt.semilogy(dicty.keys(), dicty.values(), linetype)
  else:
    plt.plot(dicty.keys(), dicty.values(), 'k')
  plt.savefig("../data/graphs/%s.png" % name)
  
def plot_xy_array(name, adicty, labels=[], xlabel=None, ylabel=None, title=None, yaxis=None, mse=False, log=False, linetype='-'):
  if linetype == 'o':
    plt.rcParams['axes.color_cycle'] = ['#282F36', '#FFFEFC', '#BDA21D', '#BFBC5B', '#D2E098']
  else:
    plt.rcParams['axes.color_cycle'] = ['b','g','r','c','m','y','k']
  plt.clf()
  if xlabel:
    plt.xlabel(xlabel)
  if ylabel:
    plt.ylabel(ylabel)
  if title:
    plt.title(title)
  # Calculate mean square error for first 2 dictionaries
  if mse:
    if len(adicty) < 2:
      print "To calculate Mean Square Error need 2 dictionaries"
    else:
      d0, d1, error, length = adicty[0], adicty[1], 0.0, len(adicty[0])
      for k in d0.keys():
        error += (d0[k]-d1[k])**2
      error /= length
      plt.figtext(0.14,0.86,"MSE: %f" % error).set_fontsize('small')
  if yaxis:
    plt.ylim(yaxis[0],yaxis[1])
  if len(labels) > 0:
    for dicty,labely in zip(adicty,labels):
      dlist = zip(*sorted(dicty.items()))
      if log:
        plt.loglog(dlist[0], dlist[1], linetype, label=labely)
      else:
        plt.plot(dlist[0], dlist[1], linetype, label=labely)
    leg = plt.legend(loc='best')
    for t in leg.get_texts():
      t.set_fontsize('small')    # the legend text fontsize
  else:
    for dicty in adicty:
      dlist = zip(*sorted(dicty.items()))
      if log:
        plt.loglog(dlist[0], dlist[1], '-')
      else:
        plt.plot(dlist[0], dlist[1], '-')
  plt.savefig("../data/graphs/%s.png" % name)