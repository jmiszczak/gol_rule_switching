#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 08:54:50 CET 2022

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
# moving average - can be used for smoothing the plots

def mav(x, w=100):
    return np.convolve(x, np.ones(w), 'valid') / w

#%% data import
# file with data from the experiment
# Note: header=6 is for NetLogo data

exp_detr = 'deterministic_realizations'
exp_rand = 'random_realizations'

df_detr = pd.read_csv(exp_detr + '.csv', header=6) 
df_rand = pd.read_csv(exp_rand + '.csv', header=6) 


#%% column names

v = [
     "[run number]",
     "synchronous",
     "init-life",
     "second-treshold",
     "rule-switch-prob",
     "world-size",
     "[step]",
     "%living"
     ]

#%%
# selected example params
init_life = 50
second_thresholds = 5,6,8
put_legend=True

# set man_n>1 to use the moving average
mav_n = 1

# mm is used to limit the numer of time steps
mm = 50

for second_threshold in second_thresholds:


    exp_desc = f'realization_il{init_life}_st{second_threshold}'
      
    
    
    #%% 
    #rule_switch_prob = 0.1
    rule_switch_probs = [_/10 for _ in [0,1,2,4,7,10]]
    
    fig = mpl.figure.Figure(figsize=(6,3.5))
    
    for i,rule_switch_prob in enumerate(rule_switch_probs):
        axs = fig.add_subplot(231+i);
        
        ed1_detr_sync = df_detr.query(f"synchronous == True & `init-life` == {init_life} & `second-threshold` == {second_threshold} & `rule-switch-prob` == 0.0")[
            ['[run number]', '[step]', '%living']]
        
        
        ed1_detr_async = df_detr.query(f"synchronous == False & `init-life` == {init_life} & `second-threshold` == {second_threshold} & `rule-switch-prob` == 0.0")[
            ['[run number]', '[step]', '%living']]
        
        
        ed1_rand_sync = df_rand.query(f"synchronous == True & `init-life` == {init_life} & `second-threshold` == {second_threshold} & `rule-switch-prob` == {rule_switch_prob}")[
            ['[run number]', '[step]', '%living']]
        
        
        ed1_rand_async = df_rand.query(f"synchronous == False & `init-life` == {init_life} & `second-threshold` == {second_threshold} & `rule-switch-prob` == {rule_switch_prob}")[
            ['[run number]', '[step]', '%living']]
        
        # number of runs where the particular cases were calculated
        
        ed1_detr_sync_r = ed1_detr_sync['[run number]'].unique()
        ed1_detr_async_r = ed1_detr_async['[run number]'].unique()
        ed1_rand_sync_r = ed1_rand_sync['[run number]'].unique()
        ed1_rand_async_r = ed1_rand_async['[run number]'].unique()
        
       
        
        for r in [12]: #iterate over realizations (just one case to show)
            ed1_detr_sync_p = ed1_detr_sync.query("`[run number]` == {}".format(ed1_detr_sync_r[r]))[['[step]', '%living']].to_numpy()
            ed1_detr_async_p = ed1_detr_async.query("`[run number]` == {}".format(ed1_detr_async_r[r]))[['[step]', '%living']].to_numpy()
            
            ed1_rand_sync_p = ed1_rand_sync.query("`[run number]` == {}".format(ed1_rand_sync_r[r]))[['[step]', '%living']].to_numpy()
            ed1_rand_async_p = ed1_rand_async.query("`[run number]` == {}".format(ed1_rand_async_r[r]))[['[step]', '%living']].to_numpy()

                        
            axs.plot(range(len( mav(ed1_detr_sync_p.T[1][1:mm+1],mav_n))), mav(ed1_detr_sync_p.T[1][1:mm+1],mav_n),'g:', label="detrm sync")
            axs.plot(range(len( mav(ed1_detr_async_p.T[1][1:mm+1],mav_n))), mav(ed1_detr_async_p.T[1][1:mm+1],mav_n), 'k-', lw=0.25, label="detrm async")
            
            axs.plot(range(len( mav(ed1_rand_sync_p.T[1][1:mm+1],mav_n))), mav(ed1_rand_sync_p.T[1][1:mm+1],mav_n),'b-.',lw=1, label="rand sync")
            axs.plot(range(len( mav(ed1_rand_async_p.T[1][1:mm+1],mav_n))), mav(ed1_rand_async_p.T[1][1:mm+1],mav_n), 'r--', lw=1.5, label="rand async")
            axs.grid(True,linestyle=':', linewidth=0.5, c='k')
            axs.set_ylim(0,100)
            axs.set_xlim(0,mm)
            axs.set_xticks(range(0,51,10))
            
            # plt.plot(ed1_p.T[0][0::], ed1_p.T[1][0::])
            
            if i not in [0,3,6]:
                axs.set_yticklabels([])
            if i in [0,3,6]:
                axs.set_ylabel('\% living')
            
            if i in [0,1,2]:
                axs.set_xticklabels([])
            if i in [3,4,5]:
                axs.set_xlabel("step")
            axs.set_title(r"$p={}$".format(rule_switch_prob))
            
            handles, labels = axs.get_legend_handles_labels()
                # lax = fig.add_axes([0.125, 1.05, 0.8, 0.025])
                # axs.legend(bbox_to_anchor=(0, 2), ncol=4)
                
    if put_legend:
        fig.legend(handles, labels, bbox_to_anchor=(0.95, 1.1), ncol=4)
        put_legend=False
        
    fig.tight_layout()
    display(fig)
    
    fName = "plots/plot_"+ exp_desc +".pdf"
    fig.savefig(fName, format="pdf", bbox_inches = 'tight')
    print("[INFO] Saving " + fName)
    