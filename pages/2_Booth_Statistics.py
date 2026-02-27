import streamlit as st
import pandas as pd
import plotly.express as px
from utils import setup_page, create_booth_data

# Setup page layout and header
setup_page("Booth Statistics - Pollytics")

# Back to home button
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("← Home", key="booth_stats_back_home", use_container_width=True):
        st.switch_page("app.py")

st.markdown("## 🏛️ Booth Level Statistics")

booth_df = create_booth_data()

# Step 1: Year Selection
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

# District and Constituency Selection (center-aligned)
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
    if selected_district and getattr(st.session_state, 'booth_constituency_dropdown', None):
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
