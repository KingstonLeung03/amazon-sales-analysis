# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 13:58:42 2025

@author: lking
"""

import sqlite3
import pandas as pd
import os

# Create data directory if it doesn't exist
os.makedirs('data', exist_ok=True)  # ← Add this line

# Load cleaned data
df = pd.read_csv("C:/Users/lking/Documents/amazon-sales-analysis/data/cleaned/amazon_clean.csv")

# Connect to SQLite database
conn = sqlite3.connect(r"C:\Users\lking\Documents\amazon-sales-analysis\data\sales.db")  # Now this path exists

# Save data to SQL table
df.to_sql("sales", conn, if_exists="replace", index=False)
conn.close()
print("Database created successfully!")