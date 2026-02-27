import streamlit as st
import pandas as pd
from pathlib import Path

# Page config
st.set_page_config(
    page_title="Pollytics - Kerala Election Analysis",
    page_icon="🗳️",
    layout="wide"
)

# Load custom CSS
def load_css():
    css_file = Path("assets/style.css")
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

# Header with ribbon
st.markdown("""
<div class="kerala-ribbon">
    <h1>🗳️ POLLYTICS</h1>
    <p>കേരള തിരഞ്ഞെടുപ്പ് വിശകലന പോർട്ടൽ | Kerala Election Analysis Portal</p>
</div>
""", unsafe_allow_html=True)

# Welcome text
st.markdown("""
<div style="text-align: center; padding: 1rem; margin-bottom: 1rem;">
    <p style="font-size: 1.1rem; color: #4A5568;">
        Comprehensive analysis of Kerala election results - transparent, accessible, and interactive
    </p>
</div>
""", unsafe_allow_html=True)

# Feature boxes in grid
st.markdown('<div class="feature-grid">', unsafe_allow_html=True)

# FIRST ROW - 3 features
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <h3>📊 Election Results</h3>
        <p>Detailed constituency-wise results with winner margins, vote percentages, and party-wise performance.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Click Here", key="results_btn"):
        st.session_state.page = "results"
        st.rerun()

with col2:
    st.markdown("""
    <div class="feature-box">
        <h3>🏛️ Booth Level Statistics</h3>
        <p>Granular booth-wise analysis including vote counts, winning candidates, and turnout percentages.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Click Here", key="booth_btn"):
        st.session_state.page = "booth"
        st.rerun()

with col3:
    st.markdown("""
    <div class="feature-box">
        <h3>👥 Candidate Performance</h3>
        <p>In-depth analysis of candidate performance across constituencies and voting patterns.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Click Here", key="candidate_btn"):
        st.session_state.page = "candidate"
        st.rerun()

# SECOND ROW - 2 features (Visual Dashboards removed)
col4, col5 = st.columns(2)

with col4:
    st.markdown("""
    <div class="feature-box">
        <h3>📈 Vote Difference Analysis</h3>
        <p>Margin analysis and close contest detection across all constituencies and booths.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Click Here", key="margin_btn"):
        st.session_state.page = "margin"
        st.rerun()

with col5:
    st.markdown("""
    <div class="feature-box">
        <h3>📍 Region Based Filtering</h3>
        <p>Filter results by district, constituency, or local body for targeted analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Click Here", key="region_btn"):
        st.session_state.page = "region"
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="
    background: linear-gradient(90deg, #1B4D3E 0%, #2E7D32 100%);
    padding: 1rem;
    margin-top: 3rem;
    text-align: center;
    color: white;
    border-radius: 5px;
">
    <p style="margin: 0;">© 2024 POLLYTICS - tinkHerHack 4.0 | Team Checkmate</p>
    <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #FFD700;">
        Data sourced from Kerala Election Commission | For hackathon demonstration only
    </p>
</div>
""", unsafe_allow_html=True)

# Page routing
if "page" not in st.session_state:
    st.session_state.page = "home"

# Placeholder pages
if st.session_state.page == "results":
    st.title("📊 Election Results Page")
    st.info("Coming soon!")
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()
elif st.session_state.page == "booth":
    st.title("🏛️ Booth Statistics")
    st.info("Coming soon!")
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()
elif st.session_state.page == "candidate":
    st.title("👥 Candidate Performance")
    st.info("Coming soon!")
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()
elif st.session_state.page == "margin":
    st.title("📈 Vote Difference Analysis")
    st.info("Coming soon!")
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()
elif st.session_state.page == "region":
    st.title("📍 Region Based Filtering")
    st.info("Coming soon!")
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()