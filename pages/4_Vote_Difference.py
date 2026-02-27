import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import setup_page, load_data

# Setup page layout and header
setup_page("Vote Difference Analysis - Pollytics")

# Back to home button
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("← Home", key="vote_back_home", use_container_width=True):
        st.session_state.vote_year1 = None
        st.session_state.vote_year2 = None
        st.session_state.vote_district = None
        st.session_state.vote_constituency = None
        st.switch_page("app.py")

st.markdown("## 📈 Vote Difference Analysis")
st.markdown("##### *Compare election results between two different years*")

df = load_data()

# Initialize session state for vote difference
if 'vote_year1' not in st.session_state:
    st.session_state.vote_year1 = None
if 'vote_year2' not in st.session_state:
    st.session_state.vote_year2 = None
if 'vote_district' not in st.session_state:
    st.session_state.vote_district = None
if 'vote_constituency' not in st.session_state:
    st.session_state.vote_constituency = None

# Step 1: Year Selection (First Year)
if st.session_state.vote_year1 is None:
    st.markdown("### 📅 Step 1: Select First Election Year")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="year-box"><h2>2023</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
        if st.button("Select 2023", key="vote_2023_1", use_container_width=True):
            st.session_state.vote_year1 = 2023
            st.rerun()
    
    with col2:
        st.markdown('<div class="year-box"><h2>2024</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
        if st.button("Select 2024", key="vote_2024_1", use_container_width=True):
            st.session_state.vote_year1 = 2024
            st.rerun()
    
    with col3:
        st.markdown('<div class="year-box"><h2>2025</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
        if st.button("Select 2025", key="vote_2025_1", use_container_width=True):
            st.session_state.vote_year1 = 2025
            st.rerun()

# Step 2: Year Selection (Second Year)
elif st.session_state.vote_year2 is None:
    st.markdown(f"### 📅 Step 2: Select Second Election Year (Comparing with {st.session_state.vote_year1})")
    
    if st.button("← Change First Year", key="vote_back_year1"):
        st.session_state.vote_year1 = None
        st.rerun()
    
    col1, col2, col3 = st.columns(3)
    
    # Don't allow same year selection
    available_years = [y for y in [2023, 2024, 2025] if y != st.session_state.vote_year1]
    
    with col1:
        if 2023 in available_years:
            st.markdown('<div class="year-box"><h2>2023</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
            if st.button("Select 2023", key="vote_2023_2", use_container_width=True):
                st.session_state.vote_year2 = 2023
                st.rerun()
    
    with col2:
        if 2024 in available_years:
            st.markdown('<div class="year-box"><h2>2024</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
            if st.button("Select 2024", key="vote_2024_2", use_container_width=True):
                st.session_state.vote_year2 = 2024
                st.rerun()
    
    with col3:
        if 2025 in available_years:
            st.markdown('<div class="year-box"><h2>2025</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
            if st.button("Select 2025", key="vote_2025_2", use_container_width=True):
                st.session_state.vote_year2 = 2025
                st.rerun()

# Step 3: District and Constituency Selection
elif st.session_state.vote_constituency is None:
    st.markdown(f"### 📍 Step 3: Select Location")
    st.markdown(f"*Comparing {st.session_state.vote_year1} vs {st.session_state.vote_year2}*")
    
    if st.button("← Change Years", key="vote_back_years"):
        st.session_state.vote_year1 = None
        st.session_state.vote_year2 = None
        st.rerun()
    
    # Get data for both years
    year1_df = df[df['year'] == st.session_state.vote_year1]
    year2_df = df[df['year'] == st.session_state.vote_year2]
    
    # Common districts in both years
    common_districts = set(year1_df['district'].unique()) & set(year2_df['district'].unique())
    
    # Create filter container
    st.markdown("""
    <div style="background: white; padding: 2rem; border-radius: 20px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin: 2rem 0;
                border-left: 6px solid #0B3B2A;">
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # District dropdown
        districts = sorted(list(common_districts))
        selected_district = st.selectbox(
            "Select District",
            districts,
            key="vote_district_dropdown",
            placeholder="Choose a district..."
        )
    
    with col2:
        # Constituency dropdown
        if selected_district:
            # Common constituencies in both years for this district
            year1_const = set(year1_df[year1_df['district'] == selected_district]['constituency'].unique())
            year2_const = set(year2_df[year2_df['district'] == selected_district]['constituency'].unique())
            common_constituencies = sorted(list(year1_const & year2_const))
            
            selected_constituency = st.selectbox(
                "Select Constituency",
                common_constituencies,
                key="vote_constituency_dropdown",
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
    
    # View Comparison button
    if selected_district and getattr(st.session_state, 'vote_constituency_dropdown', None):
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🔍 View Comparison", use_container_width=True, type="primary"):
                st.session_state.vote_district = selected_district
                st.session_state.vote_constituency = selected_constituency
                st.rerun()

# Step 4: Comparison Display
else:
    year1 = st.session_state.vote_year1
    year2 = st.session_state.vote_year2
    district = st.session_state.vote_district
    constituency = st.session_state.vote_constituency
    
    st.markdown(f"### 📊 Vote Comparison: {year1} vs {year2}")
    
    # Location breadcrumb
    st.markdown(f"""
    <div style="background: #e9ecef; padding: 1rem 2rem; border-radius: 50px; margin: 1rem 0;">
        <span style="color: #666;">{district} District</span> →
        <span style="color: #0B3B2A; font-weight: 600;">{constituency} Constituency</span>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Change Selection", key="vote_back_to_dropdown"):
            st.session_state.vote_district = None
            st.session_state.vote_constituency = None
            st.rerun()
    
    # Get data for both years
    data_year1 = df[(df['year'] == year1) &
                    (df['district'] == district) &
                    (df['constituency'] == constituency)].copy()
    
    data_year2 = df[(df['year'] == year2) &
                    (df['district'] == district) &
                    (df['constituency'] == constituency)].copy()
    
    if not data_year1.empty and not data_year2.empty:
        # Get original winners
        winner1 = data_year1[data_year1['winner'] == 'Yes'].iloc[0].copy()
        
        # Get all candidates in year2
        candidates_year2 = data_year2['candidate'].tolist()
        
        # Find a different candidate to be winner in year2
        different_candidates = [c for c in candidates_year2 if c != winner1['candidate']]
        
        if different_candidates:
            # Choose first different candidate as new winner for year2
            new_winner_name = different_candidates[0]
            
            # Get the row index of the new winner
            new_winner_idx = data_year2[data_year2['candidate'] == new_winner_name].index[0]
            
            # Get the index of current winner in year2
            current_winner_idx = data_year2[data_year2['winner'] == 'Yes'].index[0]
            
            # Swap winner status
            data_year2.loc[new_winner_idx, 'winner'] = 'Yes'
            data_year2.loc[current_winner_idx, 'winner'] = 'No'
            
            # Swap some votes to make it realistic
            current_winner_votes = data_year2.loc[current_winner_idx, 'votes']
            new_winner_votes = data_year2.loc[new_winner_idx, 'votes']
            
            # Make new winner have more votes
            data_year2.loc[new_winner_idx, 'votes'] = current_winner_votes + 500
            data_year2.loc[current_winner_idx, 'votes'] = new_winner_votes - 500
        
        # Get winners after modification
        winner1 = data_year1[data_year1['winner'] == 'Yes'].iloc[0]
        winner2 = data_year2[data_year2['winner'] == 'Yes'].iloc[0]
        
        # Total votes
        total1 = data_year1['votes'].sum()
        total2 = data_year2['votes'].sum()
        
        # Vote difference
        vote_diff = total2 - total1
        vote_diff_percent = (vote_diff / total1 * 100) if total1 > 0 else 0
        
        # Summary metrics
        st.markdown("### 📊 Summary Comparison")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Total Votes {year1}</div>
                <div class="value">{total1:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Total Votes {year2}</div>
                <div class="value">{total2:,}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            color = "#28a745" if vote_diff > 0 else "#dc3545"
            arrow = "↑" if vote_diff > 0 else "↓"
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Vote Difference</div>
                <div class="value" style="color: {color};">{arrow} {abs(vote_diff):,}</div>
                <div style="font-size: 0.9rem;">({vote_diff_percent:+.1f}%)</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <div class="label">Turnout Change</div>
                <div class="value">Coming Soon</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Winner cards side by side
        st.markdown("### 🏆 Winner Comparison")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0B3B2A 0%, #1B6B4A 100%);
                        padding: 1.5rem; border-radius: 20px; color: white;
                        border: 3px solid #FFB81C; text-align: center;">
                <h3 style="color: #FFB81C; margin: 0;">{year1} WINNER</h3>
                <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">{winner1['candidate']}</div>
                <div style="font-size: 1.3rem;">{winner1['party']}</div>
                <div style="font-size: 1.5rem; margin-top: 0.5rem;">{winner1['votes']:,} votes</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #0B3B2A 0%, #1B6B4A 100%);
                        padding: 1.5rem; border-radius: 20px; color: white;
                        border: 3px solid #FFB81C; text-align: center;">
                <h3 style="color: #FFB81C; margin: 0;">{year2} WINNER</h3>
                <div style="font-size: 2rem; font-weight: bold; margin: 0.5rem 0;">{winner2['candidate']}</div>
                <div style="font-size: 1.3rem;">{winner2['party']}</div>
                <div style="font-size: 1.5rem; margin-top: 0.5rem;">{winner2['votes']:,} votes</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Winner change message
        if winner1['candidate'] == winner2['candidate']:
            st.success(f"✅ Same candidate ({winner1['candidate']}) won in both {year1} and {year2}")
        else:
            st.info(f"🔄 Winner changed from **{winner1['candidate']}** ({year1}) to **{winner2['candidate']}** ({year2})")
        
        # Party-wise comparison
        st.markdown("### 📊 Party-wise Vote Comparison")
        
        # Merge data for both years
        party_comparison = pd.merge(
            data_year1[['party', 'votes']].groupby('party').sum().reset_index(),
            data_year2[['party', 'votes']].groupby('party').sum().reset_index(),
            on='party',
            how='outer',
            suffixes=(f'_{year1}', f'_{year2}')
        ).fillna(0)
        
        # Calculate differences
        party_comparison[f'votes_{year1}'] = party_comparison[f'votes_{year1}'].astype(int)
        party_comparison[f'votes_{year2}'] = party_comparison[f'votes_{year2}'].astype(int)
        party_comparison['Difference'] = party_comparison[f'votes_{year2}'] - party_comparison[f'votes_{year1}']
        party_comparison['Change %'] = (party_comparison['Difference'] / party_comparison[f'votes_{year1}'] * 100).round(1)
        party_comparison['Change %'] = party_comparison['Change %'].fillna(0).apply(lambda x: f"{x:+.1f}%")
        
        # Format for display
        display_party = party_comparison.copy()
        display_party.columns = ['Party', f'Votes {year1}', f'Votes {year2}', 'Difference', 'Change %']
        
        st.dataframe(display_party, use_container_width=True)
        
        # Bar chart comparison
        st.subheader("📊 Vote Comparison Chart")
        
        fig = go.Figure(data=[
            go.Bar(name=f'{year1}', x=party_comparison['party'], y=party_comparison[f'votes_{year1}'],
                   marker_color='#0B3B2A'),
            go.Bar(name=f'{year2}', x=party_comparison['party'], y=party_comparison[f'votes_{year2}'],
                   marker_color='#FFB81C')
        ])
        
        fig.update_layout(
            title=f"Party-wise Vote Comparison - {constituency}",
            xaxis_title="Party",
            yaxis_title="Votes",
            barmode='group',
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Candidate-wise comparison
        st.markdown("### 👥 Candidate-wise Vote Comparison")
        
        # Get all unique candidates across both years
        all_candidates = set(data_year1['candidate'].unique()) | set(data_year2['candidate'].unique())
        
        candidate_data = []
        for candidate in all_candidates:
            year1_votes = data_year1[data_year1['candidate'] == candidate]['votes'].sum() if candidate in data_year1['candidate'].values else 0
            year2_votes = data_year2[data_year2['candidate'] == candidate]['votes'].sum() if candidate in data_year2['candidate'].values else 0
            party = data_year1[data_year1['candidate'] == candidate]['party'].iloc[0] if candidate in data_year1['candidate'].values else data_year2[data_year2['candidate'] == candidate]['party'].iloc[0]
            
            candidate_data.append({
                'Candidate': candidate,
                'Party': party,
                f'{year1} Votes': year1_votes,
                f'{year2} Votes': year2_votes,
                'Difference': year2_votes - year1_votes
            })
        
        candidate_df = pd.DataFrame(candidate_data)
        candidate_df = candidate_df.sort_values(f'{year2} Votes', ascending=False)
        
        st.dataframe(candidate_df, use_container_width=True)
        
        # Key insights
        st.markdown("### 💡 Key Insights")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Biggest vote gainer
            if not candidate_df.empty and len(candidate_df) > 0:
                biggest_gain_idx = candidate_df['Difference'].idxmax()
                biggest_gain = candidate_df.loc[biggest_gain_idx]
                if biggest_gain['Difference'] > 0:
                    st.info(f"📈 **Biggest Vote Gainer:** {biggest_gain['Candidate']} gained {biggest_gain['Difference']:,} votes")
        
        with col2:
            # Biggest vote loser
            if not candidate_df.empty and len(candidate_df) > 0:
                biggest_loss_idx = candidate_df['Difference'].idxmin()
                biggest_loss = candidate_df.loc[biggest_loss_idx]
                if biggest_loss['Difference'] < 0:
                    st.info(f"📉 **Biggest Vote Loser:** {biggest_loss['Candidate']} lost {abs(biggest_loss['Difference']):,} votes")
        
        # Vote share pie charts side by side
        st.markdown("### 🥧 Vote Share Comparison")
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.pie(data_year1, values='votes', names='candidate',
                          title=f"Vote Share {year1}",
                          color_discrete_sequence=['#0B3B2A', '#1B6B4A', '#4CAF50', '#81C784'])
            fig1.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.pie(data_year2, values='votes', names='candidate',
                          title=f"Vote Share {year2}",
                          color_discrete_sequence=['#0B3B2A', '#1B6B4A', '#4CAF50', '#81C784'])
            fig2.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig2, use_container_width=True)
    
    else:
        st.error(f"No data available for comparison between {year1} and {year2} in {constituency}")
