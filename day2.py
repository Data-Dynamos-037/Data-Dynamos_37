#!/usr/bin/env python
# coding: utf-8

# # Step 1: Import required libraries and Dataset.

# In[2]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# In[3]:


df = pd.read_csv(r'D:\Construct Week Project\Data-Dynamos_37\pollution_us_2000_2016.csv')
df.head()


# # day 2 Duplicate data
# Check for duplicate rows
duplicates = df.duplicated().sum()
print(f"Number of duplicate rows: {duplicates}")

# Remove duplicates if they exist
df = df.drop_duplicates()


# # Convert 'Date Local' to datetime if not already

df['Date Local'] = pd.to_datetime(df['Date Local'], errors='coerce')

# Verify conversion
print(df.dtypes)


# # Check unique values in categorical columns

print("Unique values in 'State':", df['State'].unique())




