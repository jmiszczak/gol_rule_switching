#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 08:33:45 2023

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

#%% read and preprocess data
data = pd.read_csv("configurations/analyze_mutent.dat")
probs = data[(data['sync']==1) & (data['st']==4)]['p'].to_numpy()

ySync = {}
yAsync = {}

for st in [4,5,6,7,8]:
  ySync[st] = data[(data['sync']==1) & (data['st']==st)]['mutent'].to_numpy()
  yAsync[st] = data[(data['sync']==0) & (data['st']==st)]['mutent'].to_numpy()

#%% define plot styles
plot_style = {}
plot_style[4] = 'k:'
plot_style[5] = 'g--'
plot_style[6] = 'r-.'
plot_style[7] = 'c-'
plot_style[8] = 'm--'
plot_style[9] = 'y-.'

plot_marker = {}
plot_marker[4] = '+'
plot_marker[5] = '^'
plot_marker[6] = 'o'
plot_marker[7] = 'x'
plot_marker[8] = 'D'
plot_marker[9] = 's'


#%% first bunch of plots
fig = mpl.figure.Figure(figsize=(6, 3))
axsSync = fig.add_subplot(121)
axsSync.set_ylim(0.2, 1.05)
axsSync.set_title('random synchronous')
axsSync.set_xlabel('probability')
axsSync.set_ylabel('entropy')


for st in [4,5,6,7,8]:
  axsSync.plot(
    probs,
    ySync[st],
    plot_style[st], 
    marker = plot_marker[st],
    fillstyle='none', 
    ms = 8,
    label=str(st)
    )

axsSync.grid(True, linestyle=':', linewidth=0.25, c='k')
# axs.set_xticks([])
# axs.set_yticks([])
axsSync.margins()


#%% first bunch of plots
axsAsync = fig.add_subplot(122)
axsAsync.set_ylim(0.2, 1.05)
axsAsync.set_xlabel('probability')
axsAsync.set_title('random asynchronous')

for st in [4,5,6,7,8]:
  axsAsync.plot(
    probs,
    yAsync[st],
    plot_style[st], 
    marker = plot_marker[st],
    fillstyle='none', 
    ms = 8,
    label=str(st)
    )

axsAsync.grid(True, linestyle=':', linewidth=0.25, c='k')

# axs.set_xticks([])
# axs.set_yticks([])
# axsAsync.margins()


#%%

lines, labels = axsAsync.get_legend_handles_labels()

fig.legend(lines, labels, loc = 'upper center', ncol=6, bbox_to_anchor=(0.5, 1.1))

# fig.legend(loc = 'upper center', ncol=5, bbox_to_anchor=(0.5, 1.075))

fig.tight_layout()
display(fig)

#%% save the plot
fName = "plots/plot_mutent.pdf"
print("[INFO] Saving " + fName)
fig.savefig(fName, format="pdf", bbox_inches='tight')