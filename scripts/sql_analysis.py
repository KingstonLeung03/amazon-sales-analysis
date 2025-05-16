# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 14:21:55 2025

@author: lking
"""
import pandas as pd
# import numpy as np
import matplotlib as mpl  # Check matplotlib version through the main package
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

print(f"Seaborn version: {sns.__version__}")
print(f"Matplotlib version: {mpl.__version__}")  # Correct way to check version


conn = sqlite3.connect(r"C:\Users\lking\Documents\amazon-sales-analysis\data\sales.db")
cursor = conn.cursor()



q1 = '''SELECT lvl3, avg(discount_percentage) AS avg_discount
            FROM sales
            GROUP BY lvl3
            ORDER BY avg_discount
            '''


cursor.execute(q1)
results1 = cursor.fetchall()
# Convert query results to a DataFrame
df = pd.DataFrame(results1, columns=["lvl3", "avg_discount"])

# Print as a neat table
print("\n=== Top Categories by Avg. Discount ===")
print(df.to_string(index=False))

plt.figure(figsize=(10, 10))
sns.barplot(data=df, x='avg_discount', y='lvl3', hue='lvl3', 
           palette='viridis', legend=False)
plt.title('Top Categories by Avg. Discount %')
plt.tight_layout()

# Save the figure
output_path = r".\discount_analysis.png"
# plt.savefig(output_path, dpi=300, bbox_inches='tight')

q2 = '''
        SELECT product_name, rating, rating_count
            FROM sales
            WHERE rating > 4.5 AND rating_count > 1000
            ORDER BY rating_count DESC;
            '''
 
cursor.execute(q2)
results2 = cursor.fetchall()

# Convert to DataFrame and format
df_q2 = pd.DataFrame(results2, columns=["Product", "Rating", "Rating Count"])
df_q2["Product"] = df_q2["Product"].str.slice(0, 40) + "..."  # Trim to 40 chars


print("\n=== High-Rated Products with Significant Sales ===")
print(df_q2.to_string(index=False))
    
q3 = '''
        SELECT 
            CASE 
                WHEN discount_percentage > 30 THEN 'High Discount'
                WHEN discount_percentage > 10 THEN 'Medium Discount'
                ELSE 'Low Discount'
                END AS discount_group,
            AVG(rating) AS avg_rating,
            COUNT(*) AS num_products
        FROM sales
        GROUP BY discount_group;
            '''

cursor.execute(q3)
results3 = cursor.fetchall()

# Convert to DataFrame and format
df_q3 = pd.DataFrame(results3, columns=["discount_group", "avg_rating", "num_products"])
df_q3["avg_rating"] = df_q3["avg_rating"].round(2)  # Round to 2 decimals
discount_order = ['Low Discount', 'Medium Discount', 'High Discount']
df_q3['discount_group'] = pd.Categorical(df_q3['discount_group'], 
                                        categories=discount_order,
                                        ordered=True)

print("\n=== Price vs. Discount Impact Analysis ===")
print(df_q3.to_string(index=False))

q3_raw = '''
SELECT 
    rating,
    CASE 
        WHEN discount_percentage > 30 THEN 'High Discount'
        WHEN discount_percentage > 10 THEN 'Medium Discount'
        ELSE 'Low Discount'
    END AS discount_group
FROM sales
'''
cursor.execute(q3_raw)
raw_ratings = cursor.fetchall()
df_raw = pd.DataFrame(raw_ratings, columns=["rating", "discount_group"])

df_raw['discount_group'] = pd.Categorical(df_raw['discount_group'], 
                                        categories=discount_order,
                                        ordered=True)

plt.figure(figsize=(10, 6))
sns.boxplot(data=df_raw, x="discount_group", y="rating", hue="discount_group", palette="Blues")
plt.title('Does Higher Discount Hurt Ratings?')
plt.tight_layout()
output_path = r".\discount_group_ratings.png"
plt.savefig(output_path)
    
q4 = '''
       SELECT 
           product_name,
           rating_count,
           RANK() OVER (ORDER BY rating_count DESC) AS sales_rank
           FROM sales
           LIMIT 10;
            '''

cursor.execute(q4)
results4 = cursor.fetchall()

# Convert to DataFrame and format
df_q4 = pd.DataFrame(results4, columns=["Product", "Rating Count", "Sales Rank"])
df_q4["Product"] = df_q4["Product"].str.slice(0, 30) + "..."  # Trim to 30 chars


print("\n=== Rank Products by Sales ===")
print(df_q4.to_string(index=False))

# Close the connection
cursor.close()
conn.close()
plt.close()

