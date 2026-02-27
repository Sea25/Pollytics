import streamlit as st
import pandas as pd
import plotly.express as px
from utils import setup_page, load_data, render_page_header, render_breadcrumb, render_footer

setup_page("Candidate Performance - Pollytics")

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("← Home", key="cand_back_home", use_container_width=True):
        st.session_state.cand_year = None
        st.session_state.cand_district = None
        st.session_state.cand_constituency = None
        st.session_state.cand_candidate = None
        st.switch_page("app.py")

render_page_header("Candidate Performance", "Analyze individual candidate performance across constituencies", "👥")

df = load_data()

if 'cand_year' not in st.session_state:
    st.session_state.cand_year = None
if 'cand_district' not in st.session_state:
    st.session_state.cand_district = None
if 'cand_constituency' not in st.session_state:
    st.session_state.cand_constituency = None
if 'cand_candidate' not in st.session_state:
    st.session_state.cand_candidate = None

if st.session_state.cand_year is None:
    st.markdown("""
    <p style="color: #6b7280; margin-bottom: 1.5rem;">Select an election year to analyze candidate performance.</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="year-box"><h2>2023</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
        if st.button("Select 2023", key="cand_2023", use_container_width=True, type="primary"):
            st.session_state.cand_year = 2023
            st.rerun()
    
    with col2:
        st.markdown('<div class="year-box"><h2>2024</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
        if st.button("Select 2024", key="cand_2024", use_container_width=True, type="primary"):
            st.session_state.cand_year = 2024
            st.rerun()
    
    with col3:
        st.markdown('<div class="year-box"><h2>2025</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
        if st.button("Select 2025", key="cand_2025", use_container_width=True, type="primary"):
            st.session_state.cand_year = 2025
            st.rerun()

elif st.session_state.cand_constituency is None:
    render_breadcrumb([f"{st.session_state.cand_year} Election", "Select Location"])
    
    if st.button("← Change Year", key="cand_back_year"):
        st.session_state.cand_year = None
        st.rerun()
    
    year_df = df[df['year'] == st.session_state.cand_year]
    
    st.markdown("""
    <div class="filter-section">
        <div class="filter-section-title">Select Location</div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        districts = sorted(year_df['district'].unique())
        selected_district = st.selectbox(
            "District",
            options=[""] + list(districts),
            key="cand_district_dropdown",
            format_func=lambda x: "Choose a district..." if x == "" else x
        )
    
    with col2:
        if selected_district and selected_district != "":
            constituencies = sorted(year_df[year_df['district'] == selected_district]['constituency'].unique())
            selected_constituency = st.selectbox(
                "Constituency",
                options=[""] + list(constituencies),
                key="cand_constituency_dropdown",
                format_func=lambda x: "Choose a constituency..." if x == "" else x
            )
        else:
            st.selectbox(
                "Constituency",
                options=["First select a district"],
                disabled=True
            )
            selected_constituency = ""
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    if selected_district and selected_district != "" and selected_constituency and selected_constituency != "":
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("View Candidates", use_container_width=True, type="primary"):
                st.session_state.cand_district = selected_district
                st.session_state.cand_constituency = selected_constituency
                st.rerun()

elif st.session_state.cand_candidate is None:
    render_breadcrumb([f"{st.session_state.cand_year} Election", st.session_state.cand_district, st.session_state.cand_constituency, "Select Candidate"])
    
    if st.button("← Change Location", key="cand_back_location"):
        st.session_state.cand_district = None
        st.session_state.cand_constituency = None
        st.rerun()
    
    candidates_df = df[(df['year'] == st.session_state.cand_year) &
                       (df['district'] == st.session_state.cand_district) &
                       (df['constituency'] == st.session_state.cand_constituency)]
    
    st.markdown(f"""
    <p style="color: #6b7280; margin-bottom: 1rem;">
        <strong>{len(candidates_df)} candidates</strong> contested in {st.session_state.cand_constituency}
    </p>
    """, unsafe_allow_html=True)
    
    cols = st.columns(2)
    for i, (_, row) in enumerate(candidates_df.sort_values('votes', ascending=False).iterrows()):
        with cols[i % 2]:
            if row['winner'] == 'Yes':
                st.markdown(f"""
                <div class="candidate-card candidate-card-winner">
                    <div style="font-size: 1.5rem; margin-bottom: 0.5rem;">🏆</div>
                    <h3 style="margin: 0; color: #d4a03c;">{row['candidate']}</h3>
                    <p style="margin: 0.25rem 0; opacity: 0.9;">{row['party']}</p>
                    <p style="margin: 0.5rem 0 0 0; font-size: 1.25rem; font-weight: 600;">{row['votes']:,} votes</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="candidate-card">
                    <h3 style="margin: 0; color: #234d3c;">{row['candidate']}</h3>
                    <p style="margin: 0.25rem 0; color: #6b7280;">{row['party']}</p>
                    <p style="margin: 0.5rem 0 0 0; font-size: 1.25rem; font-weight: 600; color: #234d3c;">{row['votes']:,} votes</p>
                </div>
                """, unsafe_allow_html=True)
            
            if st.button(f"View Details", key=f"select_cand_{row['candidate']}", use_container_width=True):
                st.session_state.cand_candidate = row['candidate']
                st.rerun()

else:
    year = st.session_state.cand_year
    district = st.session_state.cand_district
    constituency = st.session_state.cand_constituency
    candidate_name = st.session_state.cand_candidate
    
    render_breadcrumb([f"{year} Election", district, constituency, candidate_name])
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Back to Candidates", key="cand_back_candidate"):
            st.session_state.cand_candidate = None
            st.rerun()
    
    candidate_data = df[(df['year'] == year) &
                       (df['district'] == district) &
                       (df['constituency'] == constituency) &
                       (df['candidate'] == candidate_name)].iloc[0]
    
    all_candidates = df[(df['year'] == year) &
                       (df['district'] == district) &
                       (df['constituency'] == constituency)]
    
    is_winner = candidate_data['winner'] == 'Yes'
    total_votes = all_candidates['votes'].sum()
    vote_share = (candidate_data['votes'] / total_votes) * 100
    sorted_candidates = all_candidates.sort_values('votes', ascending=False).reset_index()
    rank = sorted_candidates[sorted_candidates['candidate'] == candidate_name].index[0] + 1
    
    if is_winner:
        st.markdown(f"""
        <div class="winner-card">
            <h2>🏆 WINNER</h2>
            <div class="candidate-name">{candidate_name}</div>
            <div class="party">{candidate_data['party']}</div>
            <div class="votes">{candidate_data['votes']:,} Votes</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        winner_name = sorted_candidates.iloc[0]['candidate']
        winner_votes = sorted_candidates.iloc[0]['votes']
        margin = winner_votes - candidate_data['votes']
        
        st.markdown(f"""
        <div style="background: #f8fafc; padding: 1.5rem; border-radius: 16px; text-align: center; border: 1px solid #e2e8f0; margin-bottom: 1.5rem;">
            <h3 style="color: #1f2937; margin: 0 0 0.5rem 0;">{candidate_name}</h3>
            <p style="color: #6b7280; margin: 0;">{candidate_data['party']}</p>
            <p style="font-size: 1.5rem; font-weight: 600; color: #234d3c; margin: 0.5rem 0;">{candidate_data['votes']:,} Votes</p>
            <p style="color: #6b7280; font-size: 0.875rem; margin: 0.5rem 0 0 0;">
                Lost to {winner_name} by <strong>{margin:,}</strong> votes
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''
        <div class="stat-box">
            <div class="stat-icon">📊</div>
            <div class="stat-label">Position</div>
            <div class="stat-value">#{rank}</div>
            <div class="stat-sublabel">out of {len(all_candidates)} candidates</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="stat-box">
            <div class="stat-icon">🗳️</div>
            <div class="stat-label">Vote Share</div>
            <div class="stat-value">{vote_share:.1f}%</div>
            <div class="stat-sublabel">of total votes</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="stat-box">
            <div class="stat-icon">🏛️</div>
            <div class="stat-label">Party</div>
            <div class="stat-value" style="font-size: 1.25rem;">{candidate_data['party']}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("##### Vote Distribution")
        fig_pie = px.pie(
            all_candidates,
            values='votes',
            names='candidate',
            color_discrete_sequence=['#234d3c', '#2d6a4f', '#40916c', '#52b788', '#74c69d']
        )
        fig_pie.update_traces(
            textposition='inside',
            textinfo='percent+label',
            pull=[0.1 if x == candidate_name else 0 for x in all_candidates['candidate']]
        )
        fig_pie.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown("""
        <div style="background: #f8fafc; padding: 1rem; border-radius: 12px; border: 1px solid #e2e8f0;">
            <h4 style="color: #234d3c; margin: 0 0 0.75rem 0; font-size: 0.9rem;">How to read:</h4>
            <p style="font-size: 0.8rem; color: #4b5563; margin: 0 0 0.5rem 0;">• Bigger slice = More votes</p>
            <p style="font-size: 0.8rem; color: #4b5563; margin: 0 0 0.5rem 0;">• Selected candidate is highlighted</p>
            <p style="font-size: 0.8rem; color: #4b5563; margin: 0;">• Percentages show vote share</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("##### All Candidates Comparison")
    
    table_data = []
    for _, row in all_candidates.sort_values('votes', ascending=False).iterrows():
        winner_star = "🏆 " if row['winner'] == 'Yes' else ""
        table_data.append({
            "Candidate": f"{winner_star}{row['candidate']}",
            "Party": row['party'],
            "Votes": f"{row['votes']:,}"
        })
    
    st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    if is_winner:
        runner_up = sorted_candidates.iloc[1]['candidate']
        runner_up_votes = sorted_candidates.iloc[1]['votes']
        margin = candidate_data['votes'] - runner_up_votes
        st.success(f"**{candidate_name}** won by **{margin:,}** votes against **{runner_up}**")
    else:
        if rank == 2:
            st.info(f"**{candidate_name}** was the runner-up in this constituency")
        else:
            st.info(f"**{candidate_name}** secured position **#{rank}** in {constituency}")

render_footer()
