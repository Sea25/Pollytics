import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📍 Region Based Filtering")

# Load ONLY region_data.csv
df = pd.read_csv('data/region_data.csv')

region = st.selectbox("Select Region", df['region'].unique())
region_df = df[df['region'] == region]

st.map(region_df)  # If you have lat/long columns
st.dataframe(region_df)