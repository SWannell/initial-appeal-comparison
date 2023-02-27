# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 16:11:33 2023

@author: SWannell
"""

import matplotlib.pyplot as plt; plt.style.use('ggplot')
import matplotlib.ticker as mtick
import pandas as pd

df = pd.read_csv('AmendedData\\appeal_by_hour.csv', parse_dates=['datehour'])
df.info()

appeal_types = {'Turkey-Syria': '#ee2a24',
                'Haiti': '#850000',
                'Pakistan': '#f86652',
                'Beirut': '#652c4a',
                'Global Coronavirus': '#158aba',
                'National Emergencies Trust': '#1a3351',
                'Afghanistan': '#714200',
                'Ukraine': '#f1b13b'
                }

colour_list = [appeal_types[c] for c in df['appeal'].unique()]

# Plot the first chunk
days = 16
figs, axs = plt.subplots(2, 1, sharex=True, figsize=(8, 10))
for appeal, c in appeal_types.items():
    df_slice = df.loc[df['appeal'] == appeal, ['datehour', 'gifts']]
    df_slice.set_index('datehour', inplace=True)
    df_slice = df_slice.resample('H').sum()
    df_slice = df_slice.reset_index(drop=True)
    # Plot standard
    df_slice.loc[:days*24-1].plot(ax=axs[1], linewidth=3, color=c)
    # Plot cumu
    df_slice_cumu = df_slice.cumsum()
    df_slice_cumu.loc[:days*24-1].plot(ax=axs[0], linewidth=3, color=c)
# Check that resample is working
# [i for i in pd.date_range('2022-02-24', '2022-03-02', freq='H')[:-1] if i not in df_slice.index]
# Format the plot
thoufmt = mtick.StrMethodFormatter('{x:,.0f}')
for ax in axs:
    ax.set_xlim(0)
    ax.set_ylim(0)
    ax.yaxis.set_major_formatter(thoufmt)
# Bottom plot
axs[1].set_ylabel('Gifts')
axs[1].legend().set_visible(False)
day_range = range(0, 24*(days+1), 24)
if days < 4:
    axs[1].set_xticks(day_range)  # label the hours
    axs[1].set_title('By hour', fontsize=15)
    axs[1].set_xlabel('Hours')
else:
    xlist = [[''] * 23 + [i] for i in range(days+1)]
    xlist = [item for sublist in xlist for item in sublist]
    axs[1].set_xticks(day_range, range(0, days+1))  # label the days
    axs[1].set_title('By day', fontsize=15)
    axs[1].set_xlabel('Days')
axs[1].set_ylim(0, 2000)
# Top cumu plot
axs[0].set_ylabel('Gifts (cumulative)')
axs[0].legend(labels=appeal_types.keys())
axs[0].set_title('Cumulative', fontsize=15)
annot = "Data from Google Analytics. 'First week' starts on first 500+ gift\
 day."
figs.text(0.05, 0, annot, color='#1d1a1c', fontsize=10, alpha=0.5)
plt.suptitle('Appeal volumes from launch', fontsize=30)
plt.tight_layout()

# Save plot
last_appeal = df[df['datehour'] == df['datehour'].max()]['appeal'].values[0]
plt.savefig(f'Outputs\\first_{days}_days_{last_appeal}.png')
