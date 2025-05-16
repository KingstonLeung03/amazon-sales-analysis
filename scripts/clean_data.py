# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 17:23:41 2025

@author: lking
"""

import pandas as pd

pd.set_option('display.max_columns', 100)

raw_data = pd.read_csv('C:/Users/lking/Documents/amazon-sales-analysis/data/raw/amazon.csv')


#Delete Missing Data Rows
data = raw_data.dropna()

#Exchange Indian Rupees to New Zealand Dollar
INR_to_NZD = 0.02

data['discounted_price'] = (data['discounted_price']
                           .str.replace(',', '')
                           .str.replace('[₹NZD]', '', regex=True)
                           .astype(float) * INR_to_NZD)

data['actual_price'] = (data['actual_price']
                           .str.replace(',', '')
                           .str.replace('[₹NZD]', '', regex=True)
                           .astype(float) * INR_to_NZD)

data['rating_count'] = (data['rating_count']
                            .str.replace(',','')
                            .astype(float))

#Logical Rules Validation (delete any negative prices)


data = data[data['discounted_price'] >= 0]

data = data[data['actual_price'] >= 0]

#Specifying Currency

data['discounted_price'] = data['discounted_price'].round(2).astype(str) + ' NZD'

data['actual_price'] = data['actual_price'].round(2).astype(str) + ' NZD'



# Split hierarchy
level_categories = ['lvl1', 'lvl2', 'lvl3', 'lvl4', 'lvl5']
data[level_categories] = data['category'].str.split('|', expand=True, n=4)

# Simplify Level3 (group categories with <10% frequency into "Other")
# Compute normalized value counts
level3_counts = data['lvl3'].value_counts(normalize=True)

threshold = 10 / 100  # 0.01

mask = level3_counts > threshold

data['lvl3_Simplified'] = data['lvl3'].map(lambda x: x if mask.get(x, False) else 'Other')

# Simplify Level4 (group rare subcategories within their Level3 parent)
data['lvl4_Simplified'] = (
    data.groupby('lvl3')['lvl4']
    .transform(lambda x: x.where(x.map(x.value_counts()) >= 10, 'Other')
)
)

data['lvl5_Simplified'] = (
    data.groupby(['lvl3', 'lvl4'])['lvl5']  # Group within parent categories
    .transform(lambda x: x.where(x.map(x.value_counts()) >= 5, 'Other'))
)

print(data.head)

print(data['lvl3'].value_counts(normalize = True))

print(threshold)

data.to_csv("C:/Users/lking/Documents/amazon-sales-analysis/data/cleaned/amazon_clean.csv", index = False)

