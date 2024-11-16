import streamlit as st
import pandas as pd


data = pd.read_csv("pollution_us_2000_2016.csv")
st.write(data.head().style.set_table_styles([
    {'selector': 'thead th', 'props': [('background-color', '#1E90FF'), ('color', 'white'), ('font-size', '14px')]},
    {'selector': 'tbody td', 'props': [('background-color', '#F0F8FF'), ('color', 'black'), ('font-size', '12px')]}
]))