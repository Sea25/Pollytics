import streamlit as st
import pandas as pd
import plotly.express as px
from utils import setup_page, load_data

# Setup page layout and header
setup_page("Election Results - Pollytics")

# Back to home button
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("← Home", key="results_back_home", use_container_width=True):
        st.session_state.selected_year = None
        st.session_state.selected_district = None
        st.session_state.selected_constituency = None
        st.switch_page("app.py")

st.markdown("## 📊 Election Results")

df = load_data()

# Initialize session states
if 'selected_year' not in st.session_state:
    st.session_state.selected_year = None
if 'selected_district' not in st.session_state:
    st.session_state.selected_district = None
if 'selected_constituency' not in st.session_state:
    st.session_state.selected_constituency = None

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
    if selected_district and getattr(st.session_state, 'constituency_dropdown', None):
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
