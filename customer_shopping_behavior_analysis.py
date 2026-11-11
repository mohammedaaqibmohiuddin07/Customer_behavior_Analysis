import pandas as pd
import os

print("Current directory:", os.getcwd())

df = pd.read_csv('Project/customer_shopping_behavior.csv')

print(df.head())
df.info()
df.describe(include='all')
df.isnull().sum()
df['Review Rating'] = df.groupby('Category')['Review Rating'].transform(lambda x: x.fillna(x.median()))
df.isnull().sum()
df.columns = df.columns.str.lower()
df.columns = df.columns.str.replace(' ','_')
df = df.rename(columns={'purchase_amount_(usd)':'purchase_amount'})
df.columns
labels = ['Young Adult','Adult','Middle-Age','Senior']
df['age_group']= pd.qcut(df['age'], q=4, labels=labels)
df[['age','age_group']].head(10)

frequency_mapping = {
    'Fortnightly': 14,
    'Weekly': 7,
    'Monthly': 30,
    'Quarterly': 90,
    'Bi-Weekly': 14,
    'Annually': 365,
    'Every 3 Months': 90
}
df['purchase_frequency_days'] = df['frequency_of_purchases'].map(frequency_mapping)
df[['purchase_frequency_days','frequency_of_purchases']].head(10)
df[['discount_applied','promo_code_used']].head(10)
(df['discount_applied'] == df['promo_code_used']).all()
df.drop('promo_code_used',axis=1)
df.columns

from sqlalchemy import create_engine, URL

username = "username"
password = "Your_password"
host = "localhost"
port = "1423"
database = "customer_behavior"

connection_url = URL.create(
    "postgresql+psycopg2",
    username=username,
    password=password,
    host=host,
    port=port,
    database=database
)

engine = create_engine(connection_url)

# Test connection
with engine.connect() as connection:
    print("PostgreSQL connection successful!")

# Upload DataFrame
table_name = "customer"

df.to_sql(
    table_name,
    engine,
    if_exists="replace",
    index=False
)

print(f"Data successfully loaded into {table_name}!")
