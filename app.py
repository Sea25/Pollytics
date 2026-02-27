import folium
from streamlit_folium import folium_static
import json
import requests
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

# Load data from CSV
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('data/kerala_election_data.csv')
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Please make sure the file 'data/kerala_election_data.csv' exists in the data folder")
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

    # Feature boxes - 5 features (added Kerala Map)
    col1, col2, col3 = st.columns(3)
    col4, col5 = st.columns(2)

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
            <div class="feature-icon">🗺️</div>
            <h3>Kerala Election Map</h3>
            <p>Visualize election results across Kerala districts. See which party won where with our interactive map.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View Election Map", key="home_map", use_container_width=True):
            st.session_state.app_page = 'kerala_map'
            st.rerun()

# ---------------------------- ELECTION RESULTS PAGE ----------------------------
elif st.session_state.app_page == 'election_results':
    
    # Back to home button - FIXED: Added unique key
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Home", key="results_back_home", use_container_width=True):
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

# ---------------------------- BOOTH STATISTICS PAGE ----------------------------

    
    
        # ---------------------------- BOOTH STATISTICS PAGE ----------------------------
elif st.session_state.app_page == 'booth_stats':
    
    # Back to home button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Home", key="booth_stats_back_home", use_container_width=True):
            st.session_state.app_page = 'home'
            st.rerun()
    
    st.markdown("## 🏛️ Booth Level Statistics")
    
    # Create sample data with ALL 14 districts of Kerala and 10 booths each
    @st.cache_data
    def create_booth_data():
        # All 14 districts of Kerala
        districts = [
            'Thiruvananthapuram', 'Kollam', 'Pathanamthitta', 'Alappuzha', 'Kottayam',
            'Idukki', 'Ernakulam', 'Thrissur', 'Palakkad', 'Malappuram',
            'Kozhikode', 'Wayanad', 'Kannur', 'Kasaragod'
        ]
        
        # Major constituencies in each district
        constituencies = {
            'Thiruvananthapuram': ['Vattiyoorkavu', 'Nemom', 'Kazhakoottom', 'Kovalam', 'Parassala'],
            'Kollam': ['Kollam', 'Kundara', 'Chavara', 'Punalur', 'Karunagappally'],
            'Pathanamthitta': ['Pathanamthitta', 'Ranni', 'Aranmula', 'Konni', 'Adoor'],
            'Alappuzha': ['Alappuzha', 'Cherthala', 'Ambalappuzha', 'Haripad', 'Kayamkulam'],
            'Kottayam': ['Kottayam', 'Changanassery', 'Pala', 'Vaikom', 'Kaduthuruthy'],
            'Idukki': ['Idukki', 'Peerumade', 'Udumbanchola', 'Devikulam', 'Thodupuzha'],
            'Ernakulam': ['Ernakulam', 'Thrikkakara', 'Kalamassery', 'Paravur', 'Aluva'],
            'Thrissur': ['Thrissur', 'Ollur', 'Irinjalakuda', 'Guruvayur', 'Kodungallur'],
            'Palakkad': ['Palakkad', 'Ottapalam', 'Mannarkkad', 'Chittur', 'Alathur'],
            'Malappuram': ['Malappuram', 'Manjeri', 'Ponnani', 'Tirur', 'Perinthalmanna'],
            'Kozhikode': ['Kozhikode North', 'Kozhikode South', 'Beypore', 'Kunnamangalam', 'Koduvally'],
            'Wayanad': ['Sulthan Bathery', 'Kalpetta', 'Mananthavady', 'Vythiri', 'Panamaram'],
            'Kannur': ['Kannur', 'Thalassery', 'Payyanur', 'Taliparamba', 'Iritty'],
            'Kasaragod': ['Kasaragod', 'Kanhangad', 'Uppala', 'Manjeshwar', 'Vellarikundu']
        }
        
        data = {
            'year': [],
            'district': [],
            'constituency': [],
            'booth_id': [],
            'booth_name': [],
            'total_voters': [],
            'votes_polled': [],
            'candidate': [],
            'party': [],
            'votes': [],
            'winner': [],
            'margin': [],
            'previous_error': [],
            'postal_votes': [],
            'tendered_votes': []
        }
        
        # Generate data for each district, constituency, and booth
        booth_counter = 1
        parties = ['CPI', 'INC', 'BJP', 'CPIM', 'IUML', 'KC(M)', 'JD(S)']
        candidates = ['Suresh', 'Rajan', 'Meera', 'Anand', 'Priya', 'Manoj', 'Deepa', 
                      'Sunil', 'Bindu', 'Vijayan', 'Uma', 'George', 'Jose', 'Peter']
        
        for year in [2023, 2024, 2025]:
            for district in districts:
                district_constituencies = constituencies[district]
                # 10 booths per constituency
                for i in range(10):
                    const_index = i % len(district_constituencies)
                    constituency = district_constituencies[const_index]
                    
                    # Generate booth data
                    total = 1200 + (i * 50) + (hash(f"{district}_{i}") % 300)
                    turnout = 65 + (i * 2) + (hash(constituency) % 15)
                    if turnout > 90:
                        turnout = 90
                    votes_polled = int(total * turnout / 100)
                    
                    # Generate candidate data (3-4 candidates per booth)
                    num_candidates = 3 + (hash(f"cand_{booth_counter}") % 2)
                    remaining_votes = votes_polled
                    
                    # Determine winner (gets ~40-60% of votes)
                    winner_idx = (booth_counter + i) % len(candidates)
                    winner_name = candidates[winner_idx]
                    winner_party = parties[(winner_idx + hash(constituency)) % len(parties)]
                    winner_votes = int(votes_polled * (0.4 + (hash(f"win_{booth_counter}") % 20)/100))
                    
                    # Calculate margin (winner - runner up)
                    runner_up_votes = int((votes_polled - winner_votes) * 0.6)
                    margin = winner_votes - runner_up_votes
                    
                    for j in range(num_candidates):
                        if j == 0:  # Winner
                            candidate_name = winner_name
                            party = winner_party
                            vote_count = winner_votes
                            is_winner = 'Yes'
                            booth_margin = margin
                        else:
                            # Other candidates
                            cand_idx = (winner_idx + j + 1) % len(candidates)
                            candidate_name = candidates[cand_idx]
                            party = parties[(cand_idx + hash(constituency)) % len(parties)]
                            
                            if j == num_candidates - 1:
                                vote_count = remaining_votes - winner_votes
                            else:
                                vote_count = int((remaining_votes - winner_votes) / (num_candidates - j))
                                remaining_votes -= vote_count
                            
                            is_winner = 'No'
                            booth_margin = 0
                        
                        # Add candidate data
                        data['year'].append(year)
                        data['district'].append(district)
                        data['constituency'].append(constituency)
                        data['booth_id'].append(1000 + booth_counter)
                        data['booth_name'].append(f"Booth {booth_counter} - {['Govt. School', 'LP School', 'HSS', 'College', 'Community Hall'][i % 5]} {['North', 'South', 'East', 'West', 'Central'][i % 5]}")
                        data['total_voters'].append(total)
                        data['votes_polled'].append(votes_polled)
                        data['candidate'].append(candidate_name)
                        data['party'].append(party)
                        data['votes'].append(vote_count)
                        data['winner'].append(is_winner)
                        data['margin'].append(booth_margin)
                        data['previous_error'].append((hash(f"error_{booth_counter}") % 21))
                        data['postal_votes'].append(int(votes_polled * (2 + (hash(f"postal_{booth_counter}") % 6)) / 100))
                        data['tendered_votes'].append(hash(f"tender_{booth_counter}") % 6)
                    
                    booth_counter += 1
        
        return pd.DataFrame(data)
    
    booth_df = create_booth_data()
    
    # Step 1: Year Selection (like Election Results)
    if 'booth_selected_year' not in st.session_state:
        st.session_state.booth_selected_year = None
    if 'booth_selected_district' not in st.session_state:
        st.session_state.booth_selected_district = None
    if 'booth_selected_constituency' not in st.session_state:
        st.session_state.booth_selected_constituency = None
    
    # Year Selection
    if st.session_state.booth_selected_year is None:
        st.markdown("### Select Election Year")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="year-box"><h2>2023</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
            if st.button("Select 2023", key="booth_2023", use_container_width=True):
                st.session_state.booth_selected_year = 2023
                st.rerun()
        
        with col2:
            st.markdown('<div class="year-box"><h2>2024</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
            if st.button("Select 2024", key="booth_2024", use_container_width=True):
                st.session_state.booth_selected_year = 2024
                st.rerun()
        
        with col3:
            st.markdown('<div class="year-box"><h2>2025</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
            if st.button("Select 2025", key="booth_2025", use_container_width=True):
                st.session_state.booth_selected_year = 2025
                st.rerun()
    
    # District and Constituency Selection (center-aligned like Election Results)
    elif st.session_state.booth_selected_constituency is None:
        st.markdown(f"### 📍 {st.session_state.booth_selected_year} - Select Location")
        
        if st.button("← Change Year", key="booth_back_to_year"):
            st.session_state.booth_selected_year = None
            st.rerun()
        
        # Get data for selected year
        year_df = booth_df[booth_df['year'] == st.session_state.booth_selected_year]
        
        # Create filter container (center-aligned)
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
                key="booth_district_dropdown",
                placeholder="Choose a district..."
            )
        
        with col2:
            # Constituency dropdown
            if selected_district:
                constituencies = sorted(year_df[year_df['district'] == selected_district]['constituency'].unique())
                selected_constituency = st.selectbox(
                    "Select Constituency",
                    constituencies,
                    key="booth_constituency_dropdown",
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
        
        # View Booths button
        if selected_district and 'selected_constituency' in locals() and selected_constituency:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("🔍 View Booths", use_container_width=True, type="primary"):
                    st.session_state.booth_selected_district = selected_district
                    st.session_state.booth_selected_constituency = selected_constituency
                    st.rerun()
    
    # Booth Results Display
    else:
        year = st.session_state.booth_selected_year
        district = st.session_state.booth_selected_district
        constituency = st.session_state.booth_selected_constituency
        
        st.markdown(f"### 📊 {year} Booth Level Results")
        
        # Location breadcrumb
        st.markdown(f"""
        <div style="background: #e9ecef; padding: 1rem 2rem; border-radius: 50px; margin: 1rem 0;">
            <span style="color: #666;">{district} District</span> → 
            <span style="color: #0B3B2A; font-weight: 600;">{constituency} Constituency</span>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("← Change Selection", key="booth_back_to_dropdown"):
                st.session_state.booth_selected_district = None
                st.session_state.booth_selected_constituency = None
                st.rerun()
        
        # Get booth data for selected constituency
        booth_data = booth_df[(booth_df['year'] == year) & 
                              (booth_df['district'] == district) & 
                              (booth_df['constituency'] == constituency)]
        
        # Get unique booths
        unique_booths = booth_data[['booth_id', 'booth_name', 'total_voters', 'votes_polled', 
                                     'previous_error', 'postal_votes', 'tendered_votes']].drop_duplicates()
        
        # Get winner for each booth
        booth_winners = booth_data[booth_data['winner'] == 'Yes'][['booth_id', 'candidate', 'party', 'margin']]
        
        # Merge to get complete booth info
        booth_summary = unique_booths.merge(booth_winners, on='booth_id', how='left')
        booth_summary['turnout_percentage'] = (booth_summary['votes_polled'] / booth_summary['total_voters'] * 100).round(1)
        
        # Create tabs for different views
        tab1, tab2, tab3 = st.tabs(["📋 Booth List", "🔍 Booth Details", "📊 Polling Analysis"])
        
        with tab1:
            st.subheader(f"Booths in {constituency}")
            
            # Display booths in a nice table
            display_cols = ['booth_id', 'booth_name', 'total_voters', 'votes_polled', 'turnout_percentage', 
                           'candidate', 'party', 'margin']
            display_df = booth_summary[display_cols].copy()
            
            # Format for display
            display_df['turnout_percentage'] = display_df['turnout_percentage'].astype(str) + '%'
            display_df['margin'] = display_df['margin'].astype(str) + ' votes'
            
            # Rename columns
            display_df.columns = ['Booth ID', 'Booth Name', 'Total Voters', 'Votes Polled', 
                                 'Turnout %', 'Winner', 'Party', 'Margin']
            
            st.dataframe(display_df, use_container_width=True)
            st.info(f"Showing {len(display_df)} booths in {constituency}")
        
        with tab2:
            st.subheader("Booth Details")
            
            if not booth_summary.empty:
                # Booth selector
                booth_options = booth_summary.apply(lambda x: f"{x['booth_id']} - {x['booth_name']}", axis=1).tolist()
                selected_booth = st.selectbox("Select Booth for Detailed View", booth_options, key="booth_detail_select")
                
                # Get selected booth data
                booth_id = int(selected_booth.split(' - ')[0])
                booth_detail = booth_summary[booth_summary['booth_id'] == booth_id].iloc[0]
                
                # Display booth metrics
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Booth ID", booth_detail['booth_id'])
                    st.metric("Booth Name", booth_detail['booth_name'])
                    st.metric("Total Voters", f"{booth_detail['total_voters']:,}")
                
                with col2:
                    st.metric("Votes Polled", f"{booth_detail['votes_polled']:,}")
                    st.metric("Turnout", f"{booth_detail['turnout_percentage']}%")
                    st.metric("Postal Votes", booth_detail['postal_votes'])
                
                with col3:
                    st.metric("Winner", booth_detail['candidate'])
                    st.metric("Party", booth_detail['party'])
                    st.metric("Margin", f"{booth_detail['margin']} votes")
                
                # Get candidate-wise results for this booth
                booth_candidates = booth_data[booth_data['booth_id'] == booth_id]
                
                st.subheader("Candidate-wise Vote Split")
                
                candidates_df = booth_candidates[['candidate', 'party', 'votes']].copy()
                total_booth_votes = booth_candidates['votes'].sum()
                candidates_df['Percentage'] = (candidates_df['votes'] / total_booth_votes * 100).round(1).astype(str) + '%'
                
                st.dataframe(candidates_df, use_container_width=True)
                
                # Pie chart
                fig = px.pie(candidates_df, values='votes', names='candidate', 
                             title=f"Vote Distribution - Booth {booth_id}")
                st.plotly_chart(fig)
        
        with tab3:
            st.subheader("Polling Analysis")
            
            if not booth_summary.empty:
                # Summary metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    avg_turnout = booth_summary['turnout_percentage'].mean()
                    st.metric("Avg Turnout", f"{avg_turnout:.1f}%")
                
                with col2:
                    total_voters = booth_summary['total_voters'].sum()
                    st.metric("Total Voters", f"{total_voters:,}")
                
                with col3:
                    total_votes = booth_summary['votes_polled'].sum()
                    st.metric("Total Votes", f"{total_votes:,}")
                
                with col4:
                    total_postal = booth_summary['postal_votes'].sum()
                    st.metric("Total Postal Votes", total_postal)
                
                # Turnout comparison chart
                st.subheader("Turnout Comparison Across Booths")
                
                turnout_chart = booth_summary[['booth_id', 'turnout_percentage']].copy()
                turnout_chart['booth_id'] = turnout_chart['booth_id'].astype(str)
                turnout_chart = turnout_chart.set_index('booth_id')
                
                st.bar_chart(turnout_chart)
                
                # Detailed polling stats
                st.subheader("Polling Details by Booth")
                
                polling_stats = booth_summary[['booth_id', 'booth_name', 'total_voters', 'votes_polled', 
                                             'turnout_percentage', 'postal_votes', 'tendered_votes']].copy()
                polling_stats.columns = ['Booth ID', 'Booth Name', 'Total Voters', 'Votes Polled', 
                                        'Turnout %', 'Postal Votes', 'Tendered Votes']
                
                st.dataframe(polling_stats, use_container_width=True)
# ---------------------------- CANDIDATE PERFORMANCE PAGE ----------------------------
elif st.session_state.app_page == 'candidate_performance':
    
    # Back to home button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Home", key="cand_back_home", use_container_width=True):
            st.session_state.app_page = 'home'
            st.session_state.cand_year = None
            st.session_state.cand_district = None
            st.session_state.cand_constituency = None
            st.session_state.cand_candidate = None
            st.rerun()
    
    st.markdown("## 👥 Candidate Performance")
    st.markdown("##### *Find out how a specific candidate performed in their constituency*")
    
    # Initialize candidate session state
    if 'cand_year' not in st.session_state:
        st.session_state.cand_year = None
    if 'cand_district' not in st.session_state:
        st.session_state.cand_district = None
    if 'cand_constituency' not in st.session_state:
        st.session_state.cand_constituency = None
    if 'cand_candidate' not in st.session_state:
        st.session_state.cand_candidate = None
    
    # Step 1: Year Selection
    if st.session_state.cand_year is None:
        st.markdown("### 📅 Step 1: Choose Election Year")
        st.markdown("*Select the year of the election*")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown('<div class="year-box"><h2>2023</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
            if st.button("Select 2023", key="cand_2023", use_container_width=True):
                st.session_state.cand_year = 2023
                st.rerun()
        
        with col2:
            st.markdown('<div class="year-box"><h2>2024</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
            if st.button("Select 2024", key="cand_2024", use_container_width=True):
                st.session_state.cand_year = 2024
                st.rerun()
        
        with col3:
            st.markdown('<div class="year-box"><h2>2025</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
            if st.button("Select 2025", key="cand_2025", use_container_width=True):
                st.session_state.cand_year = 2025
                st.rerun()
    
    # Step 2: District and Constituency Selection
    elif st.session_state.cand_constituency is None:
        st.markdown(f"### 📍 Step 2: Choose Location for {st.session_state.cand_year}")
        st.markdown("*First select your district, then your constituency*")
        
        if st.button("← Change Year", key="cand_back_year"):
            st.session_state.cand_year = None
            st.rerun()
        
        # Get data for selected year
        year_df = df[df['year'] == st.session_state.cand_year]
        
        # Filter container
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
                "Select District (ജില്ല തിരഞ്ഞെടുക്കുക)",
                districts,
                key="cand_district_dropdown",
                placeholder="Choose a district..."
            )
        
        with col2:
            # Constituency dropdown
            if selected_district:
                constituencies = sorted(year_df[year_df['district'] == selected_district]['constituency'].unique())
                selected_constituency = st.selectbox(
                    "Select Constituency (നിയോജകമണ്ഡലം തിരഞ്ഞെടുക്കുക)",
                    constituencies,
                    key="cand_constituency_dropdown",
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
        
        # Next button
        if selected_district and 'selected_constituency' in locals() and selected_constituency:
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.button("👉 Next: See Candidates", use_container_width=True, type="primary"):
                    st.session_state.cand_district = selected_district
                    st.session_state.cand_constituency = selected_constituency
                    st.rerun()
    
    # Step 3: Candidate Selection
    elif st.session_state.cand_candidate is None:
        st.markdown(f"### 👥 Step 3: Choose a Candidate in {st.session_state.cand_constituency}")
        st.markdown("*Click on any candidate to see their detailed performance*")
        
        if st.button("← Change Location", key="cand_back_location"):
            st.session_state.cand_district = None
            st.session_state.cand_constituency = None
            st.rerun()
        
        # Get candidates for selected constituency
        candidates_df = df[(df['year'] == st.session_state.cand_year) & 
                           (df['district'] == st.session_state.cand_district) & 
                           (df['constituency'] == st.session_state.cand_constituency)]
        
        # Show total candidates
        st.markdown(f"**Total Candidates:** {len(candidates_df)}")
        
        # Create candidate cards in a grid
        cols = st.columns(2)
        for i, (_, row) in enumerate(candidates_df.iterrows()):
            with cols[i % 2]:
                # Different styling for winner vs others
                if row['winner'] == 'Yes':
                    # Winner card - highlighted
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #0B3B2A, #1B6B4A); 
                                padding: 1.5rem; border-radius: 15px; 
                                color: white; margin: 0.5rem 0;
                                border: 3px solid #FFB81C;">
                        <div style="font-size: 2rem; text-align: center;">🏆 WINNER</div>
                        <h3 style="text-align: center; color: #FFB81C; margin: 0.5rem 0;">{row['candidate']}</h3>
                        <p style="text-align: center; font-size: 1.2rem;">{row['party']}</p>
                        <p style="text-align: center; font-size: 1.5rem; font-weight: bold;">{row['votes']:,} votes</p>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    # Other candidates - simple card
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 15px; 
                                border: 1px solid #ddd; margin: 0.5rem 0;">
                        <h3 style="text-align: center; color: #0B3B2A;">{row['candidate']}</h3>
                        <p style="text-align: center; font-size: 1.2rem;">{row['party']}</p>
                        <p style="text-align: center; font-size: 1.3rem;">{row['votes']:,} votes</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Select button
                if st.button(f"View {row['candidate']}'s Details", key=f"select_cand_{row['candidate']}", use_container_width=True):
                    st.session_state.cand_candidate = row['candidate']
                    st.rerun()
    
    # Step 4: Candidate Performance Display
    else:
        year = st.session_state.cand_year
        district = st.session_state.cand_district
        constituency = st.session_state.cand_constituency
        candidate_name = st.session_state.cand_candidate
        
        st.markdown(f"### 📊 Performance Report: {candidate_name}")
        
        # Back button
        col1, col2 = st.columns([1, 5])
        with col1:
            if st.button("← Choose Different Candidate", key="cand_back_candidate"):
                st.session_state.cand_candidate = None
                st.rerun()
        
        # Location info in simple terms
        st.markdown(f"""
        <div style="background: #e9ecef; padding: 1rem 2rem; border-radius: 50px; margin: 1rem 0; text-align: center;">
            <span style="font-size: 1.2rem;">📍 {district} District → {constituency} Constituency</span>
        </div>
        """, unsafe_allow_html=True)
        
        # Get candidate data
        candidate_data = df[(df['year'] == year) & 
                           (df['district'] == district) & 
                           (df['constituency'] == constituency) & 
                           (df['candidate'] == candidate_name)].iloc[0]
        
        # Get all candidates in this constituency
        all_candidates = df[(df['year'] == year) & 
                           (df['district'] == district) & 
                           (df['constituency'] == constituency)]
        
        # Calculate basic stats
        is_winner = candidate_data['winner'] == 'Yes'
        total_votes = all_candidates['votes'].sum()
        vote_share = (candidate_data['votes'] / total_votes) * 100
        sorted_candidates = all_candidates.sort_values('votes', ascending=False).reset_index()
        rank = sorted_candidates[sorted_candidates['candidate'] == candidate_name].index[0] + 1
        
        # Winner/Loser message in simple terms
        if is_winner:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0B3B2A, #1B6B4A); padding: 2rem; border-radius: 20px; 
                        text-align: center; color: white; border: 4px solid #FFB81C; margin-bottom: 2rem;">
                <h1 style="font-size: 4rem; margin: 0;">🏆</h1>
                <h2 style="color: #FFB81C;">{candidate_name} WON the election!</h2>
                <p style="font-size: 1.5rem;">They received {candidate_data['votes']:,} votes</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            winner_name = sorted_candidates.iloc[0]['candidate']
            winner_votes = sorted_candidates.iloc[0]['votes']
            margin = winner_votes - candidate_data['votes']
            
            st.markdown(f"""
            <div style="background: #f8f9fa; padding: 2rem; border-radius: 20px; 
                        text-align: center; border: 2px solid #666; margin-bottom: 2rem;">
                <h2>{candidate_name} did not win</h2>
                <p style="font-size: 1.3rem;">They received {candidate_data['votes']:,} votes</p>
                <p style="font-size: 1.2rem;">The winner ({winner_name}) got {winner_votes:,} votes</p>
                <p style="font-size: 1.2rem;">Margin of defeat: {margin} votes</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Simple stats in columns
        st.markdown("### Quick Summary")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <div style="font-size: 2rem;">📊</div>
                <div style="font-size: 1.1rem; color: #666;">Position</div>
                <div style="font-size: 2rem; font-weight: bold; color: #0B3B2A;">#{rank}</div>
                <div>out of {len(all_candidates)} candidates</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <div style="font-size: 2rem;">🗳️</div>
                <div style="font-size: 1.1rem; color: #666;">Vote Share</div>
                <div style="font-size: 2rem; font-weight: bold; color: #0B3B2A;">{vote_share:.1f}%</div>
                <div>of total votes</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div style="background: white; padding: 1.5rem; border-radius: 15px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <div style="font-size: 2rem;">📋</div>
                <div style="font-size: 1.1rem; color: #666;">Party</div>
                <div style="font-size: 1.8rem; font-weight: bold; color: #0B3B2A;">{candidate_data['party']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Simple explanation
        st.markdown("---")
        st.markdown("### 📊 What do the votes look like?")
        st.markdown("*This pie chart shows how all candidates performed. The bigger the slice, the more votes they got.*")
        
        # Only pie chart - no bar graph
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Simple pie chart
            fig_pie = px.pie(
                all_candidates,
                values='votes',
                names='candidate',
                title=f"Vote Share in {constituency}",
                color_discrete_sequence=['#0B3B2A', '#1B6B4A', '#4CAF50', '#81C784', '#C8E6C9']
            )
            # Highlight selected candidate
            fig_pie.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                marker=dict(line=dict(color='#FFB81C', width=3)),
                pull=[0.1 if x == candidate_name else 0 for x in all_candidates['candidate']]
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            # Simple explanation of the pie chart
            st.markdown("""
            <div style="background: #f8f9fa; padding: 1.5rem; border-radius: 15px;">
                <h4 style="color: #0B3B2A;">How to read this chart:</h4>
                <p>• <b>Bigger slice</b> = More votes</p>
                <p>• <b>Winner's slice</b> is pulled out slightly</p>
                <p>• The <b>gold border</b> highlights the candidate you selected</p>
                <p>• Percentages show share of total votes</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Simple comparison table
        st.markdown("---")
        st.markdown("### 📋 All Candidates in This Constituency")
        st.markdown("*Listed from highest votes to lowest*")
        
        # Simple table with just essential info
        table_data = []
        for _, row in all_candidates.sort_values('votes', ascending=False).iterrows():
            winner_star = "🏆 " if row['winner'] == 'Yes' else ""
            table_data.append({
                "Candidate": f"{winner_star}{row['candidate']}",
                "Party": row['party'],
                "Votes": f"{row['votes']:,}"
            })
        
        st.table(pd.DataFrame(table_data))
        
        # Add a "Fun Fact" based on the data
        st.markdown("---")
        st.markdown("### 💡 Quick Fact")
        
        if is_winner:
            runner_up = sorted_candidates.iloc[1]['candidate']
            runner_up_votes = sorted_candidates.iloc[1]['votes']
            margin = candidate_data['votes'] - runner_up_votes
            fact = f"{candidate_name} won by {margin} votes against {runner_up}!"
        else:
            if rank == 2:
                fact = f"{candidate_name} was the runner-up! They were very close to winning."
            else:
                fact = f"{candidate_name} stood at position #{rank} in {constituency}."
        
        st.info(f"**{fact}**")

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

# ---------------------------- VOTE DIFFERENCE PAGE ----------------------------
elif st.session_state.app_page == 'vote_difference':
    
    # Back to home button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Home", key="vote_back_home", use_container_width=True):
            st.session_state.app_page = 'home'
            st.rerun()
    
    st.markdown("## 📈 Vote Difference Analysis")
    st.info("This page is under construction. Coming soon!")

# ---------------------------- KERALA MAP PAGE ----------------------------
elif st.session_state.app_page == 'kerala_map':
    
    # Back to home button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Home", key="map_back_home", use_container_width=True):
            st.session_state.app_page = 'home'
            st.rerun()
    
    st.markdown("## 🗺️ Kerala Election Map")
    st.markdown("##### *Click on any district to see who won*")
    
    # Year selector
    year = st.selectbox("Select Election Year", [2023, 2024, 2025], key="map_year")
    
    # Get data for selected year
    year_df = df[df['year'] == year]
    
    # Get winners by district
    district_winners = []
    for district in year_df['district'].unique():
        district_data = year_df[year_df['district'] == district]
        # Find the party that won most constituencies in this district
        winners = district_data[district_data['winner'] == 'Yes']
        if not winners.empty:
            top_party = winners['party'].value_counts().index[0]
            winner_name = winners[winners['party'] == top_party].iloc[0]['candidate']
        else:
            top_party = "Unknown"
            winner_name = "Unknown"
        
        total_votes = district_data['votes'].sum()
        
        district_winners.append({
            'district': district,
            'winning_party': top_party,
            'winner_name': winner_name,
            'total_votes': total_votes,
            'constituencies': len(district_data['constituency'].unique())
        })
    
    winner_df = pd.DataFrame(district_winners)
    
    # Color mapping for parties
    party_colors = {
        'CPI': '#0B3B2A',      # Dark green
        'INC': '#0000FF',       # Blue
        'BJP': '#FF9933',       # Saffron
        'IUML': '#90EE90',      # Light green
        'Unknown': '#808080'    # Grey
    }
    
    # Display districts in a grid format (since we can't use folium without installation)
    st.markdown("### 📍 District-wise Results")
    
    # Create a 3-column grid for districts
    cols = st.columns(3)
    for i, (_, row) in enumerate(winner_df.iterrows()):
        with cols[i % 3]:
            party_color = party_colors.get(row['winning_party'], '#808080')
            st.markdown(f"""
            <div style="background: white; padding: 1rem; border-radius: 10px; 
                        margin: 0.5rem 0; border-left: 6px solid {party_color};
                        box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                <h4 style="margin: 0; color: #0B3B2A;">{row['district']}</h4>
                <p style="margin: 0.3rem 0; font-size: 1.1rem;">
                    <span style="color: {party_color}; font-weight: bold;">{row['winning_party']}</span>
                </p>
                <p style="margin: 0.2rem 0; font-size: 0.9rem;">Winner: {row['winner_name']}</p>
                <p style="margin: 0; font-size: 0.9rem;">Votes: {row['total_votes']:,}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Show summary chart
    st.markdown("---")
    st.subheader("📊 Party-wise Performance")
    
    party_counts = winner_df['winning_party'].value_counts().reset_index()
    party_counts.columns = ['Party', 'Number of Districts']
    
    # Simple bar chart
    st.bar_chart(party_counts.set_index('Party'))
    
    # Data table
    with st.expander("📋 View Detailed District Data"):
        st.dataframe(winner_df, use_container_width=True)


# Footer (shown on all pages)
st.markdown("""
<div class="kerala-footer">
    <p>© 2024 POLLYTICS - tinkHerHack 4.0 | Team Checkmate</p>
    <p class="highlight">Data sourced from Kerala Election Commission | For hackathon demonstration only</p>
    <p style="font-size: 0.8rem; opacity: 0.8;">Making election data accessible to everyone</p>
</div>
""", unsafe_allow_html=True)