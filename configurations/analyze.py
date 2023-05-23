#!/usr/bin/env python
import pandas as pd
import numpy as np
import sys

#%%
# description of the experiment
golType = sys.argv[1] 

# how many files read into the data frame
# this depends on the number of available files
maxFn = 100 

# size of the grid
# this is from the configuration of the experiment
worldSize = 32 

# list of data files available for the specified experiment
dataFiles = [ "{golType}_{fn:04d}.csv".format(golType=golType, fn=fn)  for fn in range(1,maxFn+1)]

#%%
# use NetLogo format
# read only columns with coordinate and current cell state
# convert NetLogo data
# 0 is black (alive) -> 1
# 9.9 is white (dead) -> 0

# read data from the first file
data  = pd.read_csv(dataFiles[0],
                    skiprows = 15,
                    nrows = worldSize*worldSize,
                    usecols = ["pxcor", "pycor", "pcolor"])
# convert colors
data['pcolor'] = np.where(data['pcolor'] == 0, 1, 0)
# rename columns
data.rename({'pxcor' : 'x', 'pycor' : 'y', "pcolor": "s0001"}, axis='columns', inplace=True)

# append data from other files (only cell state)
for i, df in enumerate(dataFiles[1:]):
  # read data
  d  = pd.read_csv(df, 
                      skiprows = 15,
                      nrows = worldSize*worldSize,
                      usecols = ["pcolor"])
  # convert colors
  d['pcolor'] = np.where(d['pcolor'] == 0, 1, 0)
  d.rename({"pcolor": "s{:04d}".format(i+2)}, axis='columns', inplace=True)
  data = data.join(d)


#%% functions used in the analysis

def log0(x):
  if x==0:
    return 0
  else:
    return np.log2(x) 

def prob(a,x,y,data):
  pidx = data.index[(data['x']==x) & (data['y']==y) ][0]
  pd = data[(data['x'] == x) & (data['y'] == y)]
  pdt = pd.drop(['x','y'], axis=1).transpose()
  if pdt[pidx].count() > 0:
    return pdt[(pdt[pidx]==a)][pidx].count() / pdt[pidx].count()
  else:
    return 0

def jointProb(a,b,x,y,dx,dy,data):
  maxx=data['x'].max()+1
  maxy=data['y'].max()+1
  pidx = data.index[(data['x']==x) & (data['y']==y) ][0]
  nidx = data.index[(data['x']==(x+dx)%maxx) &  (data['y']==(y+dy)%maxy) ][0]
  pd = data[(data['x'].isin([x,(x+dx)%maxy])) & (data['y'].isin([y,(y+dy)%maxy]))]
  pdt = pd.drop(['x','y'], axis=1).transpose()
  if pdt[pidx].count() > 0:
    return pdt[(pdt[pidx]==a) & (pdt[nidx] == b)][pidx].count() / pdt[pidx].count()
  else:
    return 0

def condProb(a,b,x,y,dx,dy,data):
  maxx=data['x'].max()+1
  maxy=data['y'].max()+1
  if prob(b,(x+dx)%maxx,(y+dy)%maxy,data) > 0:
    return jointProb(a,b,x,y,dx,dy,data)/prob(b,(x+dx)%maxx,(y+dy)%maxy,data)
  else:
    return 0

def mutEnt(x,y,dx,dy,data):
  return -1*sum([jointProb(a,b,x,y,dx,dy,data)*log0(condProb(a,b,x,y,dx,dy,data)) for a in [0,1] for b in [0,1]])


def ptAvgMutEnt(x,y,data):
  return 0.25*(mutEnt(x,y,-1,0,data)+mutEnt(x,y,1,0,data)+mutEnt(x,y,0,-1,data)+mutEnt(x,y,0,1,data))


def avgMutEnt(data):
  maxx=data['x'].max()+1
  maxy=data['y'].max()+1
  res = 0
  for x in range(maxx):
    for y in range(maxy):
      res = res + ptAvgMutEnt(x,y,data)
  res = res / (maxx*maxy)
  return res

#%%
file = open('{}.dat'.format(golType), 'w')
file.write("{}:{}\n".format(golType,avgMutEnt(data)))
file.close()
