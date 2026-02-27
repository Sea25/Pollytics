import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Pollytics - Kerala Election Analysis",
    page_icon="🗳️",
    layout="wide"
)

# Custom CSS for Kerala government style
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+Malayalam:wght@400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #f5f7fa;
    }
    
    /* Kerala Header */
    .kerala-header {
        background: linear-gradient(135deg, #0B3B2A 0%, #1B6B4A 100%);
        padding: 2rem 2rem 2.5rem 2rem;
        margin: -1rem -1rem 2rem -1rem;
        text-align: center;
        border-bottom: 4px solid #FFB81C;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .kerala-header h1 {
        color: white;
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0;
        letter-spacing: 2px;
    }
    
    .kerala-header p {
        color: #FFB81C;
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
    }
    
    .kerala-header .malayalam {
        font-family: 'Noto Serif Malayalam', serif;
        color: rgba(255,255,255,0.9);
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* Feature Boxes */
    .feature-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        padding: 1rem;
        max-width: 1400px;
        margin: 2rem auto;
    }
    
    .feature-box {
        background: white;
        border-radius: 20px;
        padding: 2rem 1.5rem;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        border-top: 6px solid #0B3B2A;
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
    }
    
    .feature-box:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 24px rgba(11,59,42,0.2);
        border-color: #FFB81C;
    }
    
    .feature-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    .feature-box h3 {
        color: #0B3B2A;
        font-size: 1.5rem;
        font-weight: 600;
        margin: 0 0 0.5rem 0;
    }
    
    .feature-box p {
        color: #666;
        font-size: 0.95rem;
        line-height: 1.5;
        margin: 0 0 1.5rem 0;
        flex-grow: 1;
    }
    
    /* Year Boxes */
    .year-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 2rem;
        padding: 1rem;
        max-width: 1200px;
        margin: 2rem auto;
    }
    
    .year-box {
        background: white;
        border-radius: 20px;
        padding: 2.5rem 1.5rem;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        border-top: 6px solid #0B3B2A;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .year-box:hover {
        transform: translateY(-8px);
        box-shadow: 0 16px 24px rgba(11,59,42,0.2);
        border-color: #FFB81C;
    }
    
    .year-box h2 {
        color: #0B3B2A;
        font-size: 3rem;
        font-weight: 700;
        margin: 0;
    }
    
    .year-box p {
        color: #666;
        font-size: 1rem;
        margin: 0.5rem 0 0 0;
    }
    
    /* Winner Card */
    .winner-card {
        background: linear-gradient(135deg, #0B3B2A 0%, #1B6B4A 100%);
        padding: 2.5rem;
        border-radius: 30px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        border: 3px solid #FFB81C;
        box-shadow: 0 12px 24px rgba(11,59,42,0.3);
    }
    
    .winner-card h2 {
        color: #FFB81C;
        font-size: 2.5rem;
        margin: 0;
    }
    
    .winner-card .candidate-name {
        font-size: 3.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .winner-card .party {
        font-size: 1.8rem;
        opacity: 0.95;
        margin: 0.5rem 0;
    }
    
    .winner-card .votes {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 1rem 0 0 0;
    }
    
    /* Metric Cards */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        border: 1px solid #e0e0e0;
    }
    
    .metric-card .label {
        color: #666;
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .metric-card .value {
        color: #0B3B2A;
        font-size: 2rem;
        font-weight: 700;
        margin-top: 0.5rem;
    }
    
    /* Comparison Card */
    .comparison-card {
        background: white;
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 4px solid #0B3B2A;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        margin: 0.5rem 0;
    }
    
    .comparison-card .constituency {
        font-size: 1.1rem;
        font-weight: 600;
        color: #0B3B2A;
    }
    
    .comparison-card .winner {
        font-size: 1.2rem;
        color: #1B6B4A;
        font-weight: 600;
    }
    
    /* Back Button */
    .back-btn {
        background: white;
        color: #0B3B2A;
        border: 2px solid #0B3B2A;
        padding: 0.5rem 1.5rem;
        border-radius: 50px;
        font-weight: 600;
        text-decoration: none;
        display: inline-block;
        margin-bottom: 1rem;
    }
    
    .back-btn:hover {
        background: #0B3B2A;
        color: white;
    }
    
    /* Footer */
    .kerala-footer {
        background: linear-gradient(90deg, #0B3B2A 0%, #1B6B4A 100%);
        padding: 1.5rem;
        margin-top: 4rem;
        text-align: center;
        color: white;
        border-radius: 20px 20px 0 0;
    }
    
    .kerala-footer p {
        margin: 0.5rem 0;
    }
    
    .kerala-footer .highlight {
        color: #FFB81C;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="kerala-header">
    <h1>🗳️ POLLYTICS</h1>
    <p>KERALA ELECTION ANALYSIS PORTAL</p>
    <div class="malayalam">കേരള തിരഞ്ഞെടുപ്പ് വിശകലന കേന്ദ്രം</div>
</div>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/kerala_election_data.csv')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Please make sure the file 'data/kerala_election_data.csv' exists")
        return pd.DataFrame()

df = load_data()

# Initialize session state
if 'app_page' not in st.session_state:
    st.session_state.app_page = 'home'  # home, election_results, booth_stats, etc.
if 'selected_year' not in st.session_state:
    st.session_state.selected_year = None
if 'selected_district' not in st.session_state:
    st.session_state.selected_district = None
if 'selected_constituency' not in st.session_state:
    st.session_state.selected_constituency = None

# ---------------------------- HOME PAGE ----------------------------
if st.session_state.app_page == 'home':
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
            st.session_state.app_page = 'election_results'
            st.rerun()

    with col2:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">🏛️</div>
            <h3>Booth Level Statistics</h3>
            <p>Granular booth-wise analysis including vote counts, winning candidates, and detailed turnout percentages.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Booth Statistics", key="home_booth", use_container_width=True):
            st.session_state.app_page = 'booth_stats'
            st.rerun()

    with col3:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">👥</div>
            <h3>Candidate Performance</h3>
            <p>In-depth analysis of candidate performance across constituencies, vote shares, and comparative analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Candidate Performance", key="home_candidate", use_container_width=True):
            st.session_state.app_page = 'candidate_performance'
            st.rerun()

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
            st.session_state.app_page = 'vote_difference'
            st.rerun()

    with col5:
        st.markdown("""
        <div class="feature-box">
            <div class="feature-icon">📍</div>
            <h3>Region Based Filtering</h3>
            <p>Filter results by district, constituency, or local body for targeted geographical analysis.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Filter by Region", key="home_region", use_container_width=True):
            st.session_state.app_page = 'region_filtering'
            st.rerun()

# ---------------------------- ELECTION RESULTS PAGE ----------------------------
elif st.session_state.app_page == 'election_results':
    
    # Back to home button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Home", use_container_width=True):
            st.session_state.app_page = 'home'
            st.session_state.selected_year = None
            st.session_state.selected_district = None
            st.session_state.selected_constituency = None
            st.rerun()
    
    st.markdown("## 📊 Election Results")
    
    # Step 1: Year Selection
    if st.session_state.selected_year is None:
        st.markdown("### Select Election Year")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="year-box"><h2>2023</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
            if st.button("Select 2023", key="e_2023", use_container_width=True):
                st.session_state.selected_year = 2023
                st.rerun()
        
        with col2:
            st.markdown('<div class="year-box"><h2>2024</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
            if st.button("Select 2024", key="e_2024", use_container_width=True):
                st.session_state.selected_year = 2024
                st.rerun()
        
        with col3:
            st.markdown('<div class="year-box"><h2>2025</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
            if st.button("Select 2025", key="e_2025", use_container_width=True):
                st.session_state.selected_year = 2025
                st.rerun()
    
    # Step 2 & 3: District and Constituency Dropdowns
    elif st.session_state.selected_constituency is None:
        st.markdown(f"### 📍 {st.session_state.selected_year} - Select Location")
        
        if st.button("← Change Year", key="back_to_year"):
            st.session_state.selected_year = None
            st.rerun()
        
        # Get data for selected year
        year_df = df[df['year'] == st.session_state.selected_year]
        
        # Create a nice filter container
        st.markdown("""
        <div style="background: white; padding: 2rem; border-radius: 20px; 
                    box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin: 2rem 0;
                    border-left: 6px solid #0B3B2A;">
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # District dropdown
            districts = sorted(year_df['district'].unique())
            selected_district = st.selectbox(
                "Select District",
                districts,
                key="district_dropdown",
                placeholder="Choose a district..."
            )
        
        with col2:
            # Constituency dropdown (only shows after district is selected)
            if selected_district:
                constituencies = sorted(year_df[year_df['district'] == selected_district]['constituency'].unique())
                selected_constituency = st.selectbox(
                    "Select Constituency",
                    constituencies,
                    key="constituency_dropdown",
                    placeholder="Choose a constituency..."
                )
            else:
                st.selectbox(
                    "Select Constituency",
                    [],
                    disabled=True,
                    placeholder="First select a district"
                )
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # View Results button (only enabled when both are selected)
        if selected_district and 'selected_constituency' in locals() and selected_constituency:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🔍 View Results", use_container_width=True, type="primary"):
                    st.session_state.selected_district = selected_district
                    st.session_state.selected_constituency = selected_constituency
                    st.rerun()
    
    # Step 4: Results Display
    else:
        year = st.session_state.selected_year
        district = st.session_state.selected_district
        constituency = st.session_state.selected_constituency
        
        st.markdown(f"### 📊 {year} Election Results")
        
        # Location breadcrumb
        st.markdown(f"""
        <div style="background: #e9ecef; padding: 1rem 2rem; border-radius: 50px; margin: 1rem 0;">
            <span style="color: #666;">{district} District</span> → 
            <span style="color: #0B3B2A; font-weight: 600;">{constituency} Constituency</span>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("← Change Selection", key="back_to_dropdown"):
                st.session_state.selected_district = None
                st.session_state.selected_constituency = None
                st.rerun()
        
        # Get data
        const_data = df[(df['year'] == year) & 
                        (df['district'] == district) & 
                        (df['constituency'] == constituency)].copy()
        
        if not const_data.empty:
            # Find winner
            winner = const_data[const_data['winner'] == 'Yes'].iloc[0]
            runner_up = const_data[const_data['winner'] == 'No'].sort_values('votes', ascending=False).iloc[0]
            
            # Winner Card
            st.markdown(f"""
            <div class="winner-card">
                <h2>🏆 WINNER</h2>
                <div class="candidate-name">{winner['candidate']}</div>
                <div class="party">{winner['party']}</div>
                <div class="votes">{winner['votes']:,} Votes</div>
            </div>
            """, unsafe_allow_html=True)
            
            # Key Metrics
            total_votes = const_data['votes'].sum()
            margin = winner['votes'] - runner_up['votes']
            vote_share = (winner['votes'] / total_votes) * 100
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.markdown(f'<div class="metric-card"><div class="label">Total Votes</div><div class="value">{total_votes:,}</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="metric-card"><div class="label">Winning Margin</div><div class="value">{margin:,}</div></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="metric-card"><div class="label">Vote Share</div><div class="value">{vote_share:.1f}%</div></div>', unsafe_allow_html=True)
            with col4:
                st.markdown(f'<div class="metric-card"><div class="label">Runner Up</div><div class="value">{runner_up["candidate"]}</div></div>', unsafe_allow_html=True)
            
            # Charts
            st.markdown("---")
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📊 Vote Distribution")
                fig = px.bar(
                    const_data.sort_values('votes', ascending=False),
                    x='candidate',
                    y='votes',
                    color='party',
                    title=f"Vote Distribution - {constituency}",
                    color_discrete_map={'CPI': '#0B3B2A', 'INC': '#0000FF', 'BJP': '#FF9933'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("🥧 Vote Share")
                fig = px.pie(
                    const_data,
                    values='votes',
                    names='candidate',
                    title=f"Vote Share - {constituency}",
                    color_discrete_sequence=['#0B3B2A', '#1B6B4A', '#4CAF50', '#81C784', '#C8E6C9']
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
            
            # Comparison
            st.markdown("---")
            st.subheader(f"📊 Other Constituencies in {district} District")
            
            others = df[(df['year'] == year) & 
                        (df['district'] == district) & 
                        (df['constituency'] != constituency)]
            
            if not others.empty:
                other_winners = others[others['winner'] == 'Yes']
                cols = st.columns(2)
                for i, (_, row) in enumerate(other_winners.iterrows()):
                    with cols[i % 2]:
                        st.markdown(f"""
                        <div class="comparison-card">
                            <div class="constituency">{row['constituency']}</div>
                            <div class="winner">🏆 {row['candidate']} ({row['party']})</div>
                            <div style="color: #666;">{row['votes']:,} votes</div>
                        </div>
                        """, unsafe_allow_html=True)
            
            # Detailed table
            with st.expander("📋 View Detailed Results"):
                st.dataframe(
                    const_data[['candidate', 'party', 'votes']]
                    .sort_values('votes', ascending=False)
                    .reset_index(drop=True),
                    use_container_width=True
                )
        else:
            st.error("No data found for this selection")

# ---------------------------- OTHER PAGES (Placeholders) ----------------------------
elif st.session_state.app_page == 'booth_stats':
    st.markdown("## 🏛️ Booth Level Statistics")
    if st.button("← Back to Home"):
        st.session_state.app_page = 'home'
        st.rerun()
    st.info("This page is under construction. Coming soon!")

elif st.session_state.app_page == 'candidate_performance':
    st.markdown("## 👥 Candidate Performance")
    if st.button("← Back to Home"):
        st.session_state.app_page = 'home'
        st.rerun()
    st.info("This page is under construction. Coming soon!")

elif st.session_state.app_page == 'vote_difference':
    st.markdown("## 📈 Vote Difference Analysis")
    if st.button("← Back to Home"):
        st.session_state.app_page = 'home'
        st.rerun()
    st.info("This page is under construction. Coming soon!")

elif st.session_state.app_page == 'region_filtering':
    st.markdown("## 📍 Region Based Filtering")
    if st.button("← Back to Home"):
        st.session_state.app_page = 'home'
        st.rerun()
    st.info("This page is under construction. Coming soon!")

# Footer (shown on all pages)
st.markdown("""
<div class="kerala-footer">
    <p>© 2024 POLLYTICS - tinkHerHack 4.0 | Team Checkmate</p>
    <p class="highlight">Data sourced from Kerala Election Commission | For hackathon demonstration only</p>
    <p style="font-size: 0.8rem; opacity: 0.8;">Making election data accessible to everyone</p>
</div>
""", unsafe_allow_html=True)