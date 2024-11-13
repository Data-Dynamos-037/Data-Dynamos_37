# imports
import streamlit as st
import pandas as pd

# Title
st.title("US Pollution")

data = pd.read_csv("pollution_us_2000_2016.csv")

st.dataframe(data.head())