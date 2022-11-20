#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 11 07:25:46 2022

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

if len (sys.argv) > 1:
  data_file = sys.argv[1]
else:
  data_file = 'living_data.csv'

exp_desc = data_file[:-4] # remove prefix
cols = ['rand', 'sync', 'p', 'second_threshold', 'living']
data = pd.read_csv(exp_desc + '.csv', usecols = cols)

probs = []
for p in range(0,101):
    probs.append(p/100)

# used for coarsing the data
skip = 5

#%% calculate average
df = pd.DataFrame(columns=cols[:-1] + ['living_mean', 'living_min', 'living_max', 'living_std'])

for st in range(4,10):
    for r in [True, False]:
        for s in [True, False]:
            for p in probs:
               df.loc[len(df.index)] = [
                   r, s, p, st,
                    data[
                        (data['second_threshold'] == st) & 
                        (data['p'] == p) & 
                        (data['rand'] == r) & 
                        (data['sync'] == s)
                        ]['living'].mean(),
                    data[
                        (data['second_threshold'] == st) & 
                        (data['p'] == p) & 
                        (data['rand'] == r) & 
                        (data['sync'] == s)
                        ]['living'].min(),
                    data[
                        (data['second_threshold'] == st) & 
                        (data['p'] == p) & 
                        (data['rand'] == r) & 
                        (data['sync'] == s)
                        ]['living'].max(),
                    data[
                        (data['second_threshold'] == st) & 
                        (data['p'] == p) & 
                        (data['rand'] == r) & 
                        (data['sync'] == s)
                        ]['living'].std()
                    ]
               
#%% check length          
# df_len = pd.DataFrame(columns=cols)

# for st in range(4,10):
#     for r in [True, False]:
#         for s in [True, False]:
#             for p in probs:
#                df_len.loc[len(df_len.index)] = [
#                    r, s, p, st,
#                     len(data[
#                         (data['second_threshold'] == st) & 
#                         (data['p'] == p) & 
#                         (data['rand'] == r) & 
#                         (data['sync'] == s)
#                         ]['living'])]
                                   
                    
#%%
#plot_style[(rand,sync)] = 'k'
plot_style = {}
plot_style[(True,True)] = 'k:'
plot_style[(True,False)] = 'g--'
plot_style[(False,True)] = 'r-.'
plot_style[(False,False)] = 'b-'
plot_label = {}
plot_label[(True,True)] = 'rand sync'
plot_label[(True,False)] = 'rand async'
plot_label[(False,True)] = 'detrm sync'
plot_label[(False,False)] = 'detrm async'
plot_marker = {}
plot_marker[(True,True)] = 'x'
plot_marker[(True,False)] = 's'
plot_marker[(False,True)] = 'o'
plot_marker[(False,False)] = 'v'

fig = mpl.figure.Figure(figsize=(6, 4))
# l = []

for i in range(1,7):
    axs = fig.add_subplot(2,3,i)
    axs.set_xticks(np.arange(0, 1.01, 0.2))
    axs.set_ylim(-5, 105)
    axs.set_yticks(np.arange(0, 101, 20))
    axs.grid(True, linestyle=':', linewidth=0.25, c='k')

    for r in [True,False]:
        for s in [True,False]:
            plot_data_mean = df[(df['second_threshold'] == 3+i) & (df['rand'] == r) & (df['sync'] == s)]['living_mean'].to_numpy()
            # plot_data_min = df[(df['second_threshold'] == 3+i) & (df['rand'] == r) & (df['sync'] == s)]['living_min'].to_numpy()
            # plot_data_max = df[(df['second_threshold'] == 3+i) & (df['rand'] == r) & (df['sync'] == s)]['living_max'].to_numpy()
            
            axs.plot(
                probs[0:-1:skip], plot_data_mean[0:-1:skip],
                plot_style[(r,s)], linewidth=0.75, 
                marker = plot_marker[(r,s)], fillstyle='none', ms = 5,
                label=plot_label[(r,s)]
                )
            # axs.fill_between(
            #   probs[0:-1:skip], plot_data_min[0:-1:skip], plot_data_max[0:-1:skip], 
            #   linewidth=0.75, color=plot_style[(r,s)][0], alpha=0.35
            #   )
            
            axs.text(0.21,85, r"$r$={}".format(3+i),  rasterized=False, usetex=True)

    if i not in [4,5,6]:
        axs.set_xticklabels([])
    else:
        axs.set_xlabel('probability')

    if i not in [1,4]:
        axs.set_yticklabels([])
    # else:
        
    axs.set_ylabel('% of living cells')
   
    
# axs.legend(l,loc="upper", labels=plot_label.values())
lines, labels = fig.axes[-1].get_legend_handles_labels()

fig.legend(lines, labels, loc = 'upper center', ncol=4, bbox_to_anchor=(0.5, 1.05))
fig.tight_layout()
display(fig)

#%% save the firs plot
fName = "plot_" + exp_desc + "_all.pdf"
print("[INFO] Saving " + fName)
fig.savefig("plots/"+fName, format="pdf", bbox_inches='tight')


#%% plot all random and sync on one plot
plot_rs_style = {}
plot_rs_style[4] = ['k',':']
plot_rs_style[5] = ['g','--']
plot_rs_style[6] = ['r','-.']
plot_rs_style[7] = ['c','-']
plot_rs_style[8] = ['m','--']
plot_rs_style[9] = ['y','-.']

plot_rs_marker = {}
plot_rs_marker[4] = '+'
plot_rs_marker[5] = '^'
plot_rs_marker[6] = 'o'
plot_rs_marker[7] = 'x'
plot_rs_marker[8] = 'D'
plot_rs_marker[9] = 's'

fig_rs = mpl.figure.Figure(figsize=(5.5, 3))
plot_rs_text = {}
plot_rs_text[(True,True)] = 'random synchronous'
plot_rs_text[(True,False)] = 'random asynchronous'
plot_rs_text[(False,True)] = 'deterministic synchronous'
plot_rs_text[(False,False)] = 'deterministic asynchronous'

for r in [True]:
    for s in [True,False]:
        axs = fig_rs.add_subplot(122-  int(str(int(s)),base=2))
        for st in range(4,10):
            plot_data_mean = df[(df['second_threshold'] == st) & (df['rand'] == r) & (df['sync'] == s)]['living_mean'].to_numpy()
            # plot_data_min = df[(df['second_threshold'] == st) & (df['rand'] == r) & (df['sync'] == s)]['living_min'].to_numpy()
            # plot_data_max = df[(df['second_threshold'] == st) & (df['rand'] == r) & (df['sync'] == s)]['living_max'].to_numpy()
            
            # axs.fill_between(
            #   probs[0:-1:skip], plot_data_min[0:-1:skip], plot_data_max[0:-1:skip], 
            #   linewidth=0.75, color=plot_rs_style[st][0],alpha=0.35
            #   )
            axs.plot(
                probs[0:-1:skip], plot_data_mean[0:-1:skip], 
                color=plot_rs_style[st][0], linestyle=plot_rs_style[st][1],
                marker = plot_rs_marker[st], fillstyle='none', ms = 5,
                linewidth=0.75, label = r'$r={}$'.format(st)
            )
            
            axs.set_title( plot_rs_text[(r,s)],  rasterized=False, usetex=True)
            axs.set_xticks(np.arange(0, 1.01, 0.2))
            axs.set_yticks(np.arange(0, 101, 20))
            axs.set_ylim(-5, 105)
            
            axs.grid(True, linestyle=':', linewidth=0.25, c='k')

            if int(str(int(s)),base=2) == 1:            
              axs.set_ylabel('percentage of living cells')
              
            if int(str(int(s)),base=2) == 0:            
              #axs.set_ylabel('percentage of living cells')
              axs.set_yticklabels([])
              
            axs.set_xlabel('probability')        
        
lines, labels = fig_rs.axes[-1].get_legend_handles_labels()

fig_rs.legend(lines, labels, loc = 'upper center', ncol=6, bbox_to_anchor=(0.5, 1.1))
fig_rs.tight_layout()
display(fig_rs)

# if i not in [4,5,6]:
#     axs.set_xticklabels([])

# if i not in [1,4]:
#     axs.set_yticklabels([])

#%% save the firs plot
fName = "plots/plot_" + exp_desc + "_rand_sync.pdf"
print("[INFO] Saving " + fName)
fig_rs.savefig(fName, format="pdf", bbox_inches='tight')