#!/usr/bin/env python
# coding: utf-8

# # Step 1: Import required libraries and Dataset.

# In[11]:


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st


# In[12]:


df = pd.read_csv(r"W:\data dynamous2\pollution_us_2000_2016.csv")


# In[13]:


df.head()


# In[14]:


df.shape


# In[15]:


df.columns


# In[16]:


df.info()


# # Step 2: Handle Missing Data.

# # A. Identify Missing Values

# In[17]:


df.isnull().sum()


# # B. Impute Missing Data.

# In[18]:


# Drop 'Unnamed: 0' column if it's just an index
df.drop(columns=['Unnamed: 0'], inplace=True)

# Fill missing values for numerical columns with mean
numerical_columns = ['SO2 AQI', 'CO AQI']
for col in numerical_columns:
    df[col].fillna(df[col].mean(), inplace=True)
    


# In[19]:


df.isnull().sum()


# In[ ]:




