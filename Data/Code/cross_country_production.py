#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# 0. Preliminaries

# Set the current value of the PWT data file
current_pwt_file = 'pwt100.xlsx'

# Export path: Set to empty string '' if you want to export data to current directory
export_path = '../Csv/'


# 1. Import data
data = pd.read_excel('https://www.rug.nl/ggdc/docs/'+current_pwt_file,sheet_name='Data')


# 2. Metadata

# Find PWT version
info = pd.read_excel('https://www.rug.nl/ggdc/docs/'+current_pwt_file,sheet_name='Info',header=None)
legend = pd.read_excel('https://www.rug.nl/ggdc/docs/'+current_pwt_file,sheet_name='Legend',index_col=0)
version = info.iloc[0][0].split(' ')[-1]

# Find base year for real variables
base_year = legend.loc['rgdpe']['Variable definition'].split(' ')[-1].split('US')[0]

# Most recent year
final_year = data[data['countrycode']=='USA'].sort_values('year')['year'].iloc[0]

# Store metadata as Series
metadata = pd.Series(dtype=str,name='Values')
metadata['version'] = version
metadata['base_year'] = base_year
metadata['final_year'] = final_year
metadata['gdp_per_capita_units'] = base_year+' dollars per person'

# Export metadata
metadata.to_csv(export_path+'pwt_metadata.csv')


# 3. Create dataset

# Variable equals last year in data
year = data.year.iloc[-1]

# Restrict data to final year
data = data[data['year']==year].reset_index()

# Select columns: 'countrycode','country','cgdpo','emp','hc','ck'
data = data[['countrycode','country','cgdpo','emp','hc','ck']]

# Rename columns
data.columns = ['country_code','country','gdp','labor','human_capital','physical_capital']

# Drop countries with missing observations
data = data.dropna()


# 4. Export data
data[['country_code','country','gdp','labor','human_capital','physical_capital']].to_csv(export_path+'cross_country_production.csv',index=False)

