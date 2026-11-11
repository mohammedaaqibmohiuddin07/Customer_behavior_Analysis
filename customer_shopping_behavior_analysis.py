import pandas as pd
import os

print("Current directory:", os.getcwd())

df = pd.read_csv('Project/customer_shopping_behavior.csv')

print(df.head())
df.info()
