#!/usr/bin/env python
# coding: utf-8

# ----------------------------
# 1. Download dataset (Kaggle)
# ----------------------------

# !pip install kaggle
import kaggle

!kaggle datasets download ankitbansal06/retail-orders -f orders.csv


# ----------------------------
# 2. Extract ZIP file
# ----------------------------

import zipfile

with zipfile.ZipFile('orders.csv.zip', 'r') as zip_ref:
    zip_ref.extractall()


# ----------------------------
# 3. Read CSV & handle nulls
# ----------------------------

import pandas as pd

df = pd.read_csv(
    'orders.csv',
    na_values=['Not Available', 'unknown']
)


# ----------------------------
# 4. Normalize column names
# ----------------------------

df.columns = (
    df.columns
      .str.lower()
      .str.replace(' ', '_')
)


# ----------------------------
# 5. Derive business metrics
# ----------------------------

df['discount'] = df['list_price'] * df['discount_percent'] * 0.01
df['sale_price'] = df['list_price'] - df['discount']
df['profit'] = df['sale_price'] - df['cost_price']


# ----------------------------
# 6. Convert date column
# ----------------------------

df['order_date'] = pd.to_datetime(df['order_date'])


# ----------------------------
# 7. Drop redundant columns
# ----------------------------

df.drop(
    columns=['list_price', 'cost_price', 'discount_percent', 'discount'],
    inplace=True
)


# ----------------------------
# 8. Load into SQLite
# ----------------------------

import sqlite3

conn = sqlite3.connect('orders.db')

df.to_sql(
    'df_orders',
    conn,
    if_exists='replace',
    index=False
)

conn.close()
