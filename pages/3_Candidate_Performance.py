import streamlit as st
import pandas as pd
import plotly.express as px
from utils import setup_page, load_data

# Setup page layout and header
setup_page("Candidate Performance - Pollytics")

# Back to home button
col1, col2 = st.columns([1, 5])
with col1:
    if st.button("← Home", key="cand_back_home", use_container_width=True):
        st.session_state.cand_year = None
        st.session_state.cand_district = None
        st.session_state.cand_constituency = None
        st.session_state.cand_candidate = None
        st.switch_page("app.py")

st.markdown("## 👥 Candidate Performance")
st.markdown("##### *Find out how a specific candidate performed in their constituency*")

df = load_data()

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
    if selected_district and getattr(st.session_state, 'cand_constituency_dropdown', None):
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
