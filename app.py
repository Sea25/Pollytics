import streamlit as st
from utils import setup_page, render_footer

setup_page("Home - Pollytics")

st.markdown("""
<div class="hero-section">
    <div class="hero-content">
        <h1 class="hero-title">POLLYTICS</h1>
        <p class="hero-subtitle">Kerala Election Analysis Portal</p>
        <p class="hero-malayalam">കേരള തിരഞ്ഞെടുപ്പ് വിശകലന പോർട്ടൽ</p>
        
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style="text-align: center; color: #000000; font-size: 0.875rem; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 1.5rem; font-family: 'Times New Roman', Times, serif;">
    Explore Our Features
</p>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">📊</div>
        <h3>Election Results</h3>
        <p>Detailed constituency-wise results with winner margins, vote percentages, and party-wise performance analysis.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Explore Results", key="home_results", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Election_Results.py")

with col2:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">🏛️</div>
        <h3>Booth Statistics</h3>
        <p>Granular booth-level analysis including vote counts, winning candidates, turnout percentages, and polling data.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("View Booths", key="home_booth", use_container_width=True, type="primary"):
        st.switch_page("pages/2_Booth_Statistics.py")

with col3:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">👥</div>
        <h3>Candidate Performance</h3>
        <p>In-depth analysis of individual candidate performance across constituencies, including vote shares and insights.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("View Candidates", key="home_candidate", use_container_width=True, type="primary"):
        st.switch_page("pages/3_Candidate_Performance.py")

col4, col5 = st.columns(2)

with col4:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">📈</div>
        <h3>Vote Difference Analysis</h3>
        <p>Year-over-year comparison of election results. Analyze vote swings, margin changes, and party performance trends.</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Vote Difference", key="home_margin", use_container_width=True, type="primary"):
        st.switch_page("pages/4_Vote_Difference.py")

with col5:
    st.markdown("""
    <div class="feature-box">
        <div class="feature-icon">🤖</div>
        <h3>Election Chatbot</h3>
        <p>Ask questions about election results in natural language. Get instant answers about winners, margins, and more!</p>
    </div>
    """, unsafe_allow_html=True)
    if st.button("Ask Chatbot", key="home_chatbot", use_container_width=True, type="primary"):
        st.switch_page("pages/5_Election_Chatbot.py")

st.markdown("<div style='height: 2rem;'></div>", unsafe_allow_html=True)

st.markdown("""
<div style="background: #f1f5f9; border-radius: 16px; padding: 1.5rem; margin: 2rem 0; border: 1px solid #e2e8f0; font-family: 'Times New Roman', Times, serif;">
    <div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap; justify-content: center;">
        <div style="text-align: center; padding: 0.75rem 1.5rem;">
            <div style="font-size: 1.75rem; font-weight: 700; color: #234d3c;">14</div>
            <div style="font-size: 0.75rem; color: #000000; text-transform: uppercase; letter-spacing: 1px;">Districts</div>
        </div>
        <div style="width: 1px; height: 40px; background: #cbd5e1;"></div>
        <div style="text-align: center; padding: 0.75rem 1.5rem;">
            <div style="font-size: 1.75rem; font-weight: 700; color: #234d3c;">140</div>
            <div style="font-size: 0.75rem; color: #000000; text-transform: uppercase; letter-spacing: 1px;">Constituencies</div>
        </div>
        <div style="width: 1px; height: 40px; background: #cbd5e1;"></div>
        <div style="text-align: center; padding: 0.75rem 1.5rem;">
            <div style="font-size: 1.75rem; font-weight: 700; color: #234d3c;">3</div>
            <div style="font-size: 0.75rem; color: #000000; text-transform: uppercase; letter-spacing: 1px;">Election Years</div>
        </div>
        <div style="width: 1px; height: 40px; background: #cbd5e1;"></div>
        <div style="text-align: center; padding: 0.75rem 1.5rem;">
            <div style="font-size: 1.75rem; font-weight: 700; color: #234d3c;">1400+</div>
            <div style="font-size: 0.75rem; color: #000000; text-transform: uppercase; letter-spacing: 1px;">Booths Analyzed</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

render_footer()
