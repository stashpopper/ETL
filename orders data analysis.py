#!/usr/bin/env python
# coding: utf-8

"""
Retail Orders ETL Project
"""

import pandas as pd
import sqlite3
import zipfile

# ==============================================================================
# STEP 1: EXTRACT - Download and unzip data
# ==============================================================================
print("Step 1: Downloading data from Kaggle...")

import kaggle

# Download the dataset
kaggle.api.dataset_download_files(
    'ankitbansal06/retail-orders',
    path='.',
    unzip=False
)

print("✓ Downloaded orders.csv.zip")

# Unzip the file
print("\nExtracting ZIP file...")
with zipfile.ZipFile('orders.csv.zip', 'r') as zip_ref:
    zip_ref.extractall()

print("✓ Extracted orders.csv")


# ==============================================================================
# STEP 2: LOAD CSV - Read data into pandas
# ==============================================================================
print("\nStep 2: Reading CSV file...")

df = pd.read_csv('orders.csv')

print(f"✓ Loaded {len(df)} rows")
print(f"✓ Columns: {df.columns.tolist()}")


# ==============================================================================
# STEP 3: TRANSFORM - Clean and prepare data
# ==============================================================================
print("\nStep 3: Cleaning data...")

# 3.1 - Clean column names (remove spaces, make lowercase)
df.columns = df.columns.str.lower().str.replace(' ', '_')

# 3.2 - Handle missing values
df['discount_percent'] = df['discount_percent'].fillna(0)
df['quantity'] = df['quantity'].fillna(1)

# 3.3 - Fix data types
df['order_date'] = pd.to_datetime(df['order_date'])
df['list_price'] = pd.to_numeric(df['list_price'], errors='coerce')
df['cost_price'] = pd.to_numeric(df['cost_price'], errors='coerce')
df['discount_percent'] = pd.to_numeric(df['discount_percent'], errors='coerce')

# 3.4 - Remove rows with missing important data
df = df.dropna(subset=['order_id', 'order_date'])

# 3.5 - Add new calculated columns
df['discount_amount'] = df['list_price'] * (df['discount_percent'] / 100)
df['sale_price'] = df['list_price'] - df['discount_amount']
df['profit'] = df['sale_price'] - df['cost_price']

print(f"✓ Cleaned data: {len(df)} rows ready")


# ==============================================================================
# STEP 4: LOAD - Save to SQLite database
# ==============================================================================
print("\nStep 4: Loading into database...")

# Connect to database (creates file if doesn't exist)
conn = sqlite3.connect('retail_orders.db')

# Save dataframe to database
df.to_sql('df_orders', conn, if_exists='replace', index=False)

conn.close()

print("✓ Data loaded to retail_orders.db")
print("✓ Table name: df_orders")

# Quick summary
print(f"\nTotal Orders: {len(df):,}")
print(f"Total Revenue: ${df['sale_price'].sum():,.2f}")
print(f"Total Profit: ${df['profit'].sum():,.2f}")
print(f"Date Range: {df['order_date'].min()} to {df['order_date'].max()}")

print("\n✅ You can now run SQL queries on retail_orders.db")
