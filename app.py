import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Kerala Election Portal",
    page_icon="🗳️",
    layout="wide"
)

# Kerala-style header
st.markdown("""
<div style="
    background: linear-gradient(90deg, #1B4D3E 0%, #2E7D32 100%);
    padding: 2rem;
    border-radius: 5px;
    margin-bottom: 2rem;
    text-align: center;
">
    <h1 style="color: white; margin: 0;">🗳️ കേരള തിരഞ്ഞെടുപ്പ് വിശകലനം</h1>
    <p style="color: #FFD700; font-size: 1.2rem;">Kerala Election Analytics Portal</p>
</div>
""", unsafe_allow_html=True)

# Load sample data
@st.cache_data
def load_data():
    df = pd.read_csv('data/sample_data.csv')
    return df

df = load_data()

# Simple sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "Results", "Booth Analysis"])

if page == "Home":
    st.header("Welcome to Kerala Election Analytics")
    st.write("This portal provides detailed analysis of election results.")
    
    # Show quick stats
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Constituencies", df['constituency'].nunique())
    with col2:
        st.metric("Total Candidates", df['candidate'].nunique())
    with col3:
        st.metric("Total Votes", f"{df['votes'].sum():,}")

elif page == "Results":
    st.header("Election Results")
    
    # Filter by constituency
    constituency = st.selectbox("Select Constituency", df['constituency'].unique())
    
    # Filter data
    filtered_df = df[df['constituency'] == constituency]
    
    # Show results
    st.dataframe(filtered_df)
    
    # Simple chart
    fig = px.bar(filtered_df, x='candidate', y='votes', color='party', 
                 title=f"Vote Distribution - {constituency}")
    st.plotly_chart(fig)

elif page == "Booth Analysis":
    st.header("Booth Level Analysis")
    
    booth_id = st.text_input("Enter Booth ID (e.g., 101)")
    if booth_id:
        booth_df = df[df['booth_id'] == int(booth_id)]
        if not booth_df.empty:
            st.dataframe(booth_df)
            winner = booth_df[booth_df['winner'] == 'Yes']['candidate'].values[0]
            st.success(f"Winner in Booth {booth_id}: {winner}")
        else:
            st.error("Booth ID not found")

st.sidebar.markdown("---")
st.sidebar.info("tinkHerHack 4.0 | Team Checkmate")