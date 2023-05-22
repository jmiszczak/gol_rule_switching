import pandas as pd
import numpy as np


#%%
# data files
golType = 'par6_05'
maxFn = 9
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
                    nrows = 64*64,
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
                      nrows = 64*64,
                      usecols = ["pcolor"])
  # convert colors
  d['pcolor'] = np.where(d['pcolor'] == 0, 1, 0)
  d.rename({"pcolor": "s{:04d}".format(i+2)}, axis='columns', inplace=True)
  data = data.join(d)


#%%
maxx=data['x'].max()+1
maxy=data['y'].max()+1

#%% functions used in the analysis

def log0(x):
  if x==0:
    return 0
  else:
    return np.log2(x) 

def prob(a,x,y):
  pidx = data.index[(data['x']==x) & (data['y']==y) ][0]
  pd = data[(data['x'] == x) & (data['y'] == y)]
  pdt = pd.drop(['x','y'], axis=1).transpose()
  if pdt[pidx].count() > 0:
    return pdt[(pdt[pidx]==a)][pidx].count() / pdt[pidx].count()
  else:
    return 0

def jointProb(a,b,x,y,dx,dy):
  pidx = data.index[(data['x']==x) & (data['y']==y) ][0]
  nidx = data.index[(data['x']==(x+dx)%maxx) &  (data['y']==(y+dy)%maxy) ][0]
  pd = data[(data['x'].isin([x,(x+dx)%maxy])) & (data['y'].isin([y,(y+dy)%maxy]))]
  pdt = pd.drop(['x','y'], axis=1).transpose()
  if pdt[pidx].count() > 0:
    return pdt[(pdt[pidx]==a) & (pdt[nidx] == b)][pidx].count() / pdt[pidx].count()
  else:
    return 0


def condProb(a,b,x,y,dx,dy):
  if prob(b,(x+dx)%maxx,(y+dy)%maxy) > 0:
    return jointProb(a,b,x,y,dx,dy)/prob(b,(x+dx)%maxx,(y+dy)%maxy)
  else:
    return 0

def mutEnt(x,y,dx,dy):
  return -1*sum([jointProb(a,b,x,y,dx,dy)*log0(condProb(a,b,x,y,dx,dy)) for a in [0,1] for b in [0,1]])


def avgMutEnt(x,y):
  return 0.25*mutEnt(x,y,-1,0)+mutEnt(x,y,1,0)+mutEnt(x,y,0,-1)+mutEnt(x,y,0,1)

#%% sample runs
res = 0
for x in range(64):
  for y in range(64):
    res = res + avgMutEnt(x,y)
  
print(res)