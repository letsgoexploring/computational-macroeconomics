#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# 0. Preliminaries

# Set the current value of the PWT data file
current_pwt_file = 'pwt100.xlsx'

# Export path: Set to empty string '' if you want to export data to current directory
export_path = '../Csv/'


# 1. Import data
pwt = pd.read_excel('https://www.rug.nl/ggdc/docs/'+current_pwt_file,sheet_name='Data')


# 2. Manage data

# Merge country name and country code
pwt['country'] = pwt['country']+' - '+pwt['countrycode']

# Construct GDP per capita column
pwt['rgdp_pw'] = pwt['rgdpo']/pwt['emp']

# Construct GDP per worker column
pwt['rgdp_pc'] = pwt['rgdpo']/pwt['pop']

# Create array of years in data
years = pwt['year'].unique()

# Create array of countries in data
countries = pwt['country'].unique()


# 3. Construct new DataFrames and export to csv

# Iterate over two measures of GDP per person: GDP per worker and GDP per capita
for gdp_scaling in ['rgdp_pw','rgdp_pc']:
    
    # Construct empty dictionary that will be used to construct a DataFrame
    new_data = {}
    
    # Iterate over all countries
    for c in countries:
        
        # Append GDP values to dictionary
        new_data[c] = np.round(pwt[pwt['country']==c][gdp_scaling].values,2)
    
    # Construct DataFrame
    data = pd.DataFrame(new_data,index = years)
    
    # Remove observations prior to 1960 and drop missing values
    data = data.loc[1960:].dropna(axis=1)
    
    # Path of new file ()
    filepath = export_path+'cross_country_gdp_'+gdp_scaling[-2:]+'.csv'
    
    # Export data
    data.to_csv(filepath,index_label='Year')

