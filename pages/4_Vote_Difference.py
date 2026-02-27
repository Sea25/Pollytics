import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📈 Vote Difference Analysis")

# Load ONLY vote_margins.csv
df = pd.read_csv('data/vote_margins.csv')

# Show closest contests
st.subheader("🔍 Top 5 Closest Contests")
closest = df.nsmallest(5, 'margin')[['constituency', 'winner', 'runner_up', 'margin']]
st.dataframe(closest)

# Filter by district
district = st.selectbox("Select District", df['district'].unique())
district_df = df[df['district'] == district]
st.bar_chart(district_df.set_index('constituency')['margin'])