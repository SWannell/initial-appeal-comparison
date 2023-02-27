# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 17:38:35 2023

@author: SWannell
"""

import matplotlib.pyplot as plt; plt.style.use('ggplot')
import matplotlib.ticker as mtick
import pandas as pd

df = pd.read_csv('AmendedData\\appeal_by_hour_income.csv',
                 parse_dates=['date'])
df.info()

appeal_types = {'Turkey-Syria': '#ee2a24',
                'HaitiAfghanistan': '#850000',
                'Pakistan': '#f86652',
                'Beirut': '#652c4a',
                'Global Coronavirus': '#158aba',
                'National Emergencies Trust': '#1a3351',
                'Ukraine': '#f1b13b'
                }

colour_list = [appeal_types[c] for c in df['appeal'].unique()]
currfmt = mtick.StrMethodFormatter('£{x:,.0f}')

# Plot the first chunk
fig, ax = plt.subplots(1, 1, figsize=(8, 5))
for appeal, c in appeal_types.items():
    df_slice = df.loc[df['appeal'] == appeal, ['date', 'value']]
    df_slice.set_index('date', inplace=True)
    df_slice = df_slice.resample('D').sum()
    df_slice = df_slice.reset_index(drop=True)
    if appeal == 'Turkey-Syria':
        alpha = 1
    else:
        alpha = 0.5
    df_slice.plot(ax=ax, linewidth=3, color=c, alpha=alpha)
ax.yaxis.set_major_formatter(currfmt)
ax.set_xlim(0)
ax.set_ylim(0, 100000)
ax.set_xlabel('Day')
ax.set_ylabel('Income')
ax.legend(labels=appeal_types.keys())
ax.set_title('Platform daytime unpaid income from "launch"', fontsize=20)
annot = f"Data from Google Analytics. 'Launch' starts on first 500+ gift \
day, and only covers 'unpaid' channels\n between 08:00-17:00. Income to all \
appeals counted."
fig.text(0.05, -0.05, annot, color='#1d1a1c', fontsize=10, alpha=0.5)
ax.axhline(20000, color='black')
plt.tight_layout()

# Save plot
plt.savefig(f'Outputs\\income_drop_first_month.png')
