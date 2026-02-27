import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Election Results")

# Load ONLY election_results.csv
df = pd.read_csv('data/election_results.csv')

# Rest of the code...