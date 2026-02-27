import streamlit as st
from utils import setup_page

# Setup page layout and header
setup_page("Home - Pollytics")

st.markdown("""
<div style="text-align: center; padding: 1rem 2rem; margin-bottom: 1rem;">
    <p style="font-size: 1.2rem; color: #4A5568; max-width: 800px; margin: 0 auto;">
        Comprehensive analysis of Kerala election results - transparent, accessible, and interactive
    </p>
</div>
""", unsafe_allow_html=True)

# Feature boxes
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">📊</div>
        <h3>Election Results</h3>
        <p>Detailed constituency-wise results with winner margins, vote percentages, and party-wise performance analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("View Election Results", key="home_results", use_container_width=True):
        st.switch_page("pages/1_Election_Results.py")

with col2:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">🏛️</div>
        <h3>Booth Level Statistics</h3>
        <p>Granular booth-wise analysis including vote counts, winning candidates, and detailed turnout percentages.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("View Booth Statistics", key="home_booth", use_container_width=True):
        st.switch_page("pages/2_Booth_Statistics.py")

with col3:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">👥</div>
        <h3>Candidate Performance</h3>
        <p>In-depth analysis of candidate performance across constituencies, vote shares, and comparative analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("View Candidate Performance", key="home_candidate", use_container_width=True):
        st.switch_page("pages/3_Candidate_Performance.py")

col4, col5 = st.columns(2)

with col4:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">📈</div>
        <h3>Vote Difference Analysis</h3>
        <p>Margin analysis and close contest detection across all constituencies and booths with visual indicators.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("View Vote Differences", key="home_margin", use_container_width=True):
        st.switch_page("pages/4_Vote_Difference.py")

with col5:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">📍</div>
        <h3>Kerala Election Map</h3>
        <p>Interactive district-wise election map offering visual, geographical analysis of election results.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("View Election Map", key="home_region", use_container_width=True):
        st.switch_page("pages/5_Kerala_Map.py")
