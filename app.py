import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
    else:
        # Fallback CSS
        st.markdown("""
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
            @import url('https://fonts.googleapis.com/css2?family=Noto+Serif+Malayalam:wght@400;500;600;700&display=swap');
            
            .stApp {
                font-family: 'Inter', sans-serif;
                background-color: #f5f7fa;
            }
            
            /* Kerala Style Header */
            .kerala-ribbon {
                background: linear-gradient(135deg, #0B3B2A 0%, #1B6B4A 100%);
                padding: 2rem 2rem 2.5rem 2rem;
                margin: -5rem -4rem 2rem -4rem;
                text-align: center;
                border-bottom: 4px solid #FFB81C;
                box-shadow: 0 8px 20px rgba(0,40,20,0.2);
                clip-path: polygon(0 0, 100% 0, 100% 85%, 50% 100%, 0 85%);
            }
            
            .kerala-ribbon h1 {
                color: white;
                font-size: 3.5rem;
                font-weight: 700;
                margin: 0;
                letter-spacing: 2px;
                text-shadow: 3px 3px 0 rgba(0,0,0,0.1);
            }
            
            .kerala-ribbon .subhead {
                color: #FFB81C;
                font-size: 1.3rem;
                margin: 0.5rem 0 0 0;
                font-weight: 500;
                letter-spacing: 2px;
            }
            
            .kerala-ribbon .malayalam {
                font-family: 'Noto Serif Malayalam', serif;
                color: rgba(255,255,255,0.9);
                font-size: 1.2rem;
                margin-top: 0.5rem;
            }
            
            /* Year Selection Boxes - Like Home Page */
            .year-grid {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 2rem;
                padding: 2rem 4rem;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .year-box {
                background: white;
                border-radius: 16px;
                padding: 2.5rem 1.5rem;
                text-align: center;
                transition: all 0.3s ease;
                border: 1px solid #e0e0e0;
                box-shadow: 0 8px 16px -4px rgba(0,0,0,0.1);
                cursor: pointer;
                border-top: 6px solid #0B3B2A;
            }
            
            .year-box:hover {
                transform: translateY(-8px);
                box-shadow: 0 20px 30px -8px rgba(11,59,42,0.3);
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
                margin-top: 0.5rem;
            }
            
            /* Filter Section Styling */
            .filter-container {
                background: white;
                padding: 2rem;
                border-radius: 20px;
                box-shadow: 0 8px 20px rgba(0,0,0,0.05);
                margin: 2rem 0;
                border: 1px solid #e0e0e0;
                border-left: 6px solid #0B3B2A;
            }
            
            .filter-title {
                color: #0B3B2A;
                font-size: 1.5rem;
                font-weight: 600;
                margin-bottom: 1.5rem;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid #FFB81C;
            }
            
            /* Winner Card */
            .winner-card {
                background: linear-gradient(135deg, #0B3B2A 0%, #1B6B4A 100%);
                padding: 2rem;
                border-radius: 20px;
                color: white;
                text-align: center;
                margin: 2rem 0;
                box-shadow: 0 12px 24px -8px rgba(11,59,42,0.4);
                border: 2px solid #FFB81C;
            }
            
            .winner-card h3 {
                font-size: 2.5rem;
                margin: 0;
                color: #FFB81C;
            }
            
            .winner-card .party {
                font-size: 1.3rem;
                opacity: 0.9;
                margin: 0.5rem 0;
            }
            
            .winner-card .votes {
                font-size: 2rem;
                font-weight: 700;
                margin: 1rem 0 0 0;
            }
            
            /* Comparison Cards */
            .comparison-grid {
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 1.5rem;
                margin: 2rem 0;
            }
            
            .comparison-card {
                background: white;
                padding: 1.5rem;
                border-radius: 16px;
                border: 1px solid #e0e0e0;
                border-left: 4px solid #0B3B2A;
                box-shadow: 0 4px 12px rgba(0,0,0,0.05);
            }
            
            .comparison-card h4 {
                color: #0B3B2A;
                margin: 0 0 0.5rem 0;
                font-size: 1.2rem;
            }
            
            .comparison-card .winner-name {
                font-size: 1.3rem;
                font-weight: 600;
                color: #1B6B4A;
            }
            
            .comparison-card .votes {
                color: #666;
                font-size: 1.1rem;
            }
            
            /* Back Button */
            .back-btn {
                background: white;
                color: #0B3B2A;
                border: 2px solid #0B3B2A;
                padding: 0.6rem 1.5rem;
                border-radius: 50px;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                margin-bottom: 1rem;
            }
            
            .back-btn:hover {
                background: #0B3B2A;
                color: white;
            }
            
            /* Stats Cards */
            .stats-container {
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 1rem;
                margin: 2rem 0;
            }
            
            .stat-card {
                background: #f8f9fa;
                padding: 1.2rem;
                border-radius: 12px;
                text-align: center;
                border: 1px solid #e0e0e0;
            }
            
            .stat-card .label {
                color: #666;
                font-size: 0.9rem;
                text-transform: uppercase;
            }
            
            .stat-card .value {
                color: #0B3B2A;
                font-size: 1.5rem;
                font-weight: 700;
                margin-top: 0.3rem;
            }
        </style>
        """, unsafe_allow_html=True)

load_css()

# ---------------------------- BACKEND FUNCTIONS ----------------------------
@st.cache_data
def load_election_data():
    """Load election data from CSV"""
    try:
        df = pd.read_csv('data/kerala_election_results.csv')
        return df
    except:
        # Return sample data if file not found
        return pd.DataFrame({
            'year': [2024, 2024, 2024, 2024, 2023, 2023],
            'constituency': ['Thiruvananthapuram', 'Thiruvananthapuram', 'Vattiyoorkavu', 'Vattiyoorkavu', 'Thiruvananthapuram', 'Vattiyoorkavu'],
            'district': ['Thiruvananthapuram', 'Thiruvananthapuram', 'Thiruvananthapuram', 'Thiruvananthapuram', 'Thiruvananthapuram', 'Thiruvananthapuram'],
            'candidate': ['Suresh', 'Rajan', 'Krishnan', 'Sudheer', 'Suresh', 'Krishnan'],
            'party': ['CPI', 'INC', 'CPI', 'INC', 'CPI', 'CPI'],
            'votes': [45892, 42341, 38923, 35678, 42500, 36500],
            'winner': ['Yes', 'No', 'Yes', 'No', 'Yes', 'Yes'],
            'booth_count': [142, 142, 98, 98, 142, 98],
            'electors': [245000, 245000, 180000, 180000, 245000, 180000]
        })

def get_winner_for_constituency(df, year, constituency):
    """Get winner details for a specific constituency and year"""
    data = df[(df['year'] == year) & (df['constituency'] == constituency)]
    winner = data[data['winner'] == 'Yes'].iloc[0] if not data[data['winner'] == 'Yes'].empty else None
    return winner

def get_all_constituencies_in_district(df, year, district):
    """Get all constituencies in a district for a given year"""
    return df[(df['year'] == year) & (df['district'] == district)]['constituency'].unique()

def get_comparison_data(df, year, district, current_constituency):
    """Get winner data for all constituencies in district except current"""
    all_const = get_all_constituencies_in_district(df, year, district)
    comparison = []
    for const in all_const:
        if const != current_constituency:
            winner = get_winner_for_constituency(df, year, const)
            if winner is not None:
                comparison.append({
                    'constituency': const,
                    'winner': winner['candidate'],
                    'party': winner['party'],
                    'votes': winner['votes']
                })
    return comparison

# ---------------------------- PAGE FUNCTIONS ----------------------------
def show_home_page():
    """Home page with feature boxes"""
    st.markdown("""
    <div class="kerala-ribbon">
        <h1>🗳️ POLLYTICS</h1>
        <div class="subhead">KERALA ELECTION ANALYSIS PORTAL</div>
        <div class="malayalam">കേരള തിരഞ്ഞെടുപ്പ് വിശകലന കേന്ദ്രം</div>
    </div>
    """, unsafe_allow_html=True)

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
        <div class="feature-box" style="padding: 2rem;">
            <h3 style="font-size: 2rem;">📊</h3>
            <h3>Election Results</h3>
            <p>Detailed constituency-wise results with winner analysis and inter-constituency comparison.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Click Here", key="results_btn"):
            st.session_state.page = "results_year"
            st.rerun()

    with col2:
        st.markdown("""
        <div class="feature-box" style="padding: 2rem;">
            <h3 style="font-size: 2rem;">🏛️</h3>
            <h3>Booth Level Statistics</h3>
            <p>Granular booth-wise analysis including vote counts and winning candidates.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Click Here", key="booth_btn"):
            st.session_state.page = "booth"
            st.rerun()

    with col3:
        st.markdown("""
        <div class="feature-box" style="padding: 2rem;">
            <h3 style="font-size: 2rem;">👥</h3>
            <h3>Candidate Performance</h3>
            <p>In-depth analysis of candidate performance across constituencies.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Click Here", key="candidate_btn"):
            st.session_state.page = "candidate"
            st.rerun()

    col4, col5 = st.columns(2)

    with col4:
        st.markdown("""
        <div class="feature-box" style="padding: 2rem;">
            <h3 style="font-size: 2rem;">📈</h3>
            <h3>Vote Difference Analysis</h3>
            <p>Margin analysis and close contest detection across constituencies.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Click Here", key="margin_btn"):
            st.session_state.page = "margin"
            st.rerun()

    with col5:
        st.markdown("""
        <div class="feature-box" style="padding: 2rem;">
            <h3 style="font-size: 2rem;">📍</h3>
            <h3>Region Based Filtering</h3>
            <p>Filter results by district, constituency, or local body.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Click Here", key="region_btn"):
            st.session_state.page = "region"
            st.rerun()
    
    # Footer
    st.markdown("""
    <div style="
        background: linear-gradient(90deg, #0B3B2A 0%, #1B6B4A 100%);
        padding: 1.5rem;
        margin-top: 4rem;
        text-align: center;
        color: white;
        border-radius: 12px 12px 0 0;
    ">
        <p style="margin: 0; font-size: 1.1rem;">© 2024 POLLYTICS - tinkHerHack 4.0 | Team Checkmate</p>
        <p style="margin: 0.5rem 0 0 0; font-size: 0.9rem; color: #FFB81C;">
            Data sourced from Kerala Election Commission | For hackathon demonstration only
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_year_selection():
    """Page 1: Select Election Year"""
    st.markdown("""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
        <h1 style="color: #0B3B2A; margin:0;">📊 Election Results</h1>
    </div>
    """, unsafe_allow_html=True)
    
    if st.button("← Back to Home", key="back_home_year"):
        st.session_state.page = "home"
        st.rerun()
    
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; margin: 2rem 0;">
        <h2 style="color: #0B3B2A;">Select Election Year</h2>
        <p style="color: #666;">Choose a year to view detailed results</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Year selection boxes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="year-box">
            <h2>2023</h2>
            <p>Assembly Election</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View 2023 Results", key="year_2023"):
            st.session_state.selected_year = 2023
            st.session_state.page = "results_filter"
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="year-box">
            <h2>2024</h2>
            <p>Assembly Election</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View 2024 Results", key="year_2024"):
            st.session_state.selected_year = 2024
            st.session_state.page = "results_filter"
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="year-box">
            <h2>2025</h2>
            <p>Assembly Election</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("View 2025 Results", key="year_2025"):
            st.session_state.selected_year = 2025
            st.session_state.page = "results_filter"
            st.rerun()

def show_filter_page():
    """Page 2: Filter by District and Constituency"""
    year = st.session_state.selected_year
    df = load_election_data()
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
        <h1 style="color: #0B3B2A; margin:0;">📊 {year} Election Results</h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back to Years", key="back_years"):
            st.session_state.page = "results_year"
            st.rerun()
    with col2:
        if st.button("🏠 Home", key="home_from_filter"):
            st.session_state.page = "home"
            st.rerun()
    
    st.markdown("---")
    
    # Filter Section
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    st.markdown('<div class="filter-title">📍 Select Location</div>', unsafe_allow_html=True)
    
    # Get unique districts for selected year
    year_data = df[df['year'] == year]
    districts = sorted(year_data['district'].unique())
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("##### District")
        selected_district = st.selectbox("", districts, key="district_filter", label_visibility="collapsed")
    
    with col2:
        st.markdown("##### Constituency")
        # Get constituencies for selected district and year
        const_data = year_data[year_data['district'] == selected_district]
        constituencies = sorted(const_data['constituency'].unique())
        selected_constituency = st.selectbox("", constituencies, key="const_filter", label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # View Results Button
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("🔍 View Analysis", use_container_width=True, type="primary"):
            st.session_state.selected_district = selected_district
            st.session_state.selected_constituency = selected_constituency
            st.session_state.page = "results_analysis"
            st.rerun()

def show_analysis_page():
    """Page 3: Show winner and comparison"""
    year = st.session_state.selected_year
    district = st.session_state.selected_district
    constituency = st.session_state.selected_constituency
    df = load_election_data()
    
    # Get winner data
    winner = get_winner_for_constituency(df, year, constituency)
    
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 2rem;">
        <h1 style="color: #0B3B2A; margin:0;">📊 {year} Results</h1>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back to Filters", key="back_filters"):
            st.session_state.page = "results_filter"
            st.rerun()
    with col2:
        if st.button("🏠 Home", key="home_from_analysis"):
            st.session_state.page = "home"
            st.rerun()
    
    st.markdown("---")
    
    # Location breadcrumb
    st.markdown(f"""
    <div style="background: #f0f2f5; padding: 0.8rem 1.5rem; border-radius: 50px; margin: 1rem 0;">
        <span style="color: #666;">{district} District</span> → 
        <span style="color: #0B3B2A; font-weight: 600;">{constituency} Constituency</span>
    </div>
    """, unsafe_allow_html=True)
    
    if winner is not None:
        # Winner Card (Only Winner - No Runner Up)
        st.markdown(f"""
        <div class="winner-card">
            <h3>🏆 {winner['candidate']}</h3>
            <div class="party">{winner['party']}</div>
            <div class="votes">{winner['votes']:,} Votes</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Quick Stats
        const_data = df[(df['year'] == year) & (df['constituency'] == constituency)]
        total_votes = const_data['votes'].sum()
        turnout = (total_votes / const_data['electors'].iloc[0]) * 100 if 'electors' in const_data.columns else None
        booth_count = const_data['booth_count'].iloc[0] if 'booth_count' in const_data.columns else 'N/A'
        
        st.markdown("""
        <div class="stats-container">
        """, unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"""
            <div class="stat-card">
                <div class="label">Total Votes</div>
                <div class="value">{total_votes:,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
            <div class="stat-card">
                <div class="label">Winner Margin</div>
                <div class="value">{winner['votes'] - const_data[const_data['winner'] == 'No']['votes'].max():,}</div>
            </div>
            """, unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div class="stat-card">
                <div class="label">Turnout</div>
                <div class="value">{turnout:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
        with col4:
            st.markdown(f"""
            <div class="stat-card">
                <div class="label">Booths</div>
                <div class="value">{booth_count}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Comparison with other constituencies in same district
        st.markdown(f"""
        <div style="margin: 3rem 0 1.5rem 0;">
            <h2 style="color: #0B3B2A; border-left: 6px solid #FFB81C; padding-left: 1rem;">
                📊 Comparison with Other Constituencies in {district}
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        comparison = get_comparison_data(df, year, district, constituency)
        
        if comparison:
            cols = st.columns(2)
            for i, const_data in enumerate(comparison):
                with cols[i % 2]:
                    st.markdown(f"""
                    <div class="comparison-card">
                        <h4>{const_data['constituency']}</h4>
                        <div class="winner-name">🏆 {const_data['winner']}</div>
                        <div class="votes">{const_data['party']} • {const_data['votes']:,} votes</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Simple chart showing winner's vote share
        st.markdown("""
        <div style="margin: 3rem 0 1.5rem 0;">
            <h2 style="color: #0B3B2A; border-left: 6px solid #FFB81C; padding-left: 1rem;">
                📈 Vote Distribution
            </h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Prepare data for pie chart
        pie_data = const_data[['candidate', 'votes']].copy()
        fig = px.pie(
            pie_data,
            values='votes',
            names='candidate',
            title=f"Vote Share - {constituency}",
            color_discrete_sequence=['#1B4D3E', '#4CAF50', '#81C784', '#C8E6C9', '#A5D6A7']
        )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        st.error("No data found for this constituency")

def show_other_pages(page_name):
    """Placeholder for other pages"""
    st.title(f"{page_name}")
    st.info("This page is under construction. Coming soon!")
    if st.button("← Back to Home"):
        st.session_state.page = "home"
        st.rerun()

# ---------------------------- MAIN APP ----------------------------
# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "home"
if "selected_year" not in st.session_state:
    st.session_state.selected_year = 2024
if "selected_district" not in st.session_state:
    st.session_state.selected_district = None
if "selected_constituency" not in st.session_state:
    st.session_state.selected_constituency = None

# Page routing
if st.session_state.page == "home":
    show_home_page()
elif st.session_state.page == "results_year":
    show_year_selection()
elif st.session_state.page == "results_filter":
    show_filter_page()
elif st.session_state.page == "results_analysis":
    show_analysis_page()
elif st.session_state.page == "booth":
    show_other_pages("🏛️ Booth Level Statistics")
elif st.session_state.page == "candidate":
    show_other_pages("👥 Candidate Performance")
elif st.session_state.page == "margin":
    show_other_pages("📈 Vote Difference Analysis")
elif st.session_state.page == "region":
    show_other_pages("📍 Region Based Filtering")