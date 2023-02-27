# -*- coding: utf-8 -*-
"""
Created on Mon Feb  6 15:57:13 2023

@author: SWannell
"""

import pandas as pd
import pickle

fp = r'RawData\\_First_ week income for appeals.xlsx'

xls = pd.ExcelFile(fp)
sheets = xls.sheet_names
sheets = sheets[2:]

col_names = {
    'Product': 'page',
    'Hour of Day': 'datehour',
    'Unique Purchases': 'gifts'
        }

df_dict = dict([])
for sheet in sheets:
    df = pd.read_excel(xls, sheet, skiprows=14)
    df.drop(list(df.filter(regex='Unnamed')), axis=1, inplace=True)
    df.rename(col_names, inplace=True, axis=1)
    df['datehour'] = pd.to_datetime(df['datehour'], format='%Y%m%d%H')
    df['appeal'] = sheet
    df_dict[sheet] = df

xls.close()

with open('AmendedData\\dfdict.pickle', 'wb') as handle:
    pickle.dump(df_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

df = pd.concat(df_dict.values(), sort=False)
df.reset_index(inplace=True, drop=True)
df = df.groupby(['appeal', 'datehour']).sum()
df.to_csv('AmendedData\\appeal_by_hour.csv')
