#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 17:52:12 2022

@author: jam
"""

#%% global packages
import sys

import pandas as pd
import numpy as np

import matplotlib as mpl
import matplotlib.colors as colors
import matplotlib.figure as figure

mpl.rc('text', usetex=True)
mpl.rc('font', family='serif')
mpl.rc('font', size=10)

from IPython.core.display import display

#%%

world_size = 64
if len (sys.argv) > 1:
  world_name = sys.argv[1]
else:
  world_name = 'world_size{}_init50_sync_detr_dp2_st7.csv'.format(world_size)

data = pd.read_csv("" + world_name + '',
                   skiprows=15, 
                   nrows=world_size*world_size,
                   usecols = ["pcolor"]
                   )

data = data.to_numpy()
data = np.reshape(data,(world_size,world_size))

#%%
fig = mpl.figure.Figure(figsize=(6, 5.5))

axs = fig.add_subplot(111)

#%%
axs.matshow(data, cmap=colors.ListedColormap(["black", 'white']))

axs.spines['top'].set_visible(False)
axs.spines['right'].set_visible(False)
axs.spines['bottom'].set_visible(False)
axs.spines['left'].set_visible(False)

axs.set_xticks([])
axs.set_yticks([])
axs.margins()

#%%
fig.tight_layout()
display(fig)

fName = "plots/plot_" + world_name.replace(".csv","") + ".pdf"
print("[INFO] Saving " + fName)
fig.savefig(fName, format="pdf", bbox_inches='tight')
