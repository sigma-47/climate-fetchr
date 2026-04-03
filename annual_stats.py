#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 08:02:45 2026

@author: jay
"""

import pandas as pd
from matplotlib import pyplot as plt
import os


infile = "klawitter_daily_weather_1995-2024"

df = pd.read_csv(infile, index_col=0, parse_dates=True)

df['temperature_mean'] = (df['temperature_2m_max']+df['temperature_2m_min'])/2.

df['precip_liq'] = df['precipitation_sum']
df.loc[(df['temperature_mean']<=32),'precip_liq'] = 0

df['precip_frz'] = df['precipitation_sum']
df.loc[(df['temperature_mean']>32),'precip_frz'] = 0

yrly_df = df[['precipitation_sum','precip_liq', 'precip_frz']].resample('YE').sum()

qtil_df = yrly_df.quantile([0.1,0.25,0.5,0.75,0.9])

cols = ['precipitation_sum','precip_liq', 'precip_frz']

fig, axes = plt.subplots(nrows=len(cols), ncols=1, figsize=(8, 4 * len(cols)))

for ax, col in zip(axes, cols):
    yrly_df.boxplot(column=col, ax=ax)
    # Custom labels per axis
    ax.set_title("Annual {0}".format(col))
    ax.set_ylabel('Inches')
    #ax.set_xlabel(col)
    
plt.tight_layout() # Fixes overlapping labels
plt.show()