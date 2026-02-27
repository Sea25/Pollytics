import streamlit as st
import pandas as pd
import plotly.express as px
from utils import setup_page, create_booth_data, render_page_header, render_breadcrumb, render_footer

setup_page("Booth Statistics - Pollytics")

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("← Home", key="booth_stats_back_home", use_container_width=True):
        st.switch_page("app.py")

render_page_header("Booth Statistics", "Granular booth-level analysis with turnout and polling data", "🏛️")

booth_df = create_booth_data()

if 'booth_selected_year' not in st.session_state:
    st.session_state.booth_selected_year = None
if 'booth_selected_district' not in st.session_state:
    st.session_state.booth_selected_district = None
if 'booth_selected_constituency' not in st.session_state:
    st.session_state.booth_selected_constituency = None

if st.session_state.booth_selected_year is None:
    st.markdown("""
    <p style="color: #6b7280; margin-bottom: 1.5rem;">Select an election year to view booth-level statistics.</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="year-box"><h2>2023</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
        if st.button("Select 2023", key="booth_2023", use_container_width=True, type="primary"):
            st.session_state.booth_selected_year = 2023
            st.rerun()
    
    with col2:
        st.markdown('<div class="year-box"><h2>2024</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
        if st.button("Select 2024", key="booth_2024", use_container_width=True, type="primary"):
            st.session_state.booth_selected_year = 2024
            st.rerun()
    
    with col3:
        st.markdown('<div class="year-box"><h2>2025</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
        if st.button("Select 2025", key="booth_2025", use_container_width=True, type="primary"):
            st.session_state.booth_selected_year = 2025
            st.rerun()

elif st.session_state.booth_selected_constituency is None:
    render_breadcrumb([f"{st.session_state.booth_selected_year} Election", "Select Location"])
    
    if st.button("← Change Year", key="booth_back_to_year"):
        st.session_state.booth_selected_year = None
        st.rerun()
    
    year_df = booth_df[booth_df['year'] == st.session_state.booth_selected_year]
    
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
            key="booth_district_dropdown",
            format_func=lambda x: "Choose a district..." if x == "" else x
        )
    
    with col2:
        if selected_district and selected_district != "":
            constituencies = sorted(year_df[year_df['district'] == selected_district]['constituency'].unique())
            selected_constituency = st.selectbox(
                "Constituency",
                options=[""] + list(constituencies),
                key="booth_constituency_dropdown",
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
            if st.button("View Booths", use_container_width=True, type="primary"):
                st.session_state.booth_selected_district = selected_district
                st.session_state.booth_selected_constituency = selected_constituency
                st.rerun()

else:
    year = st.session_state.booth_selected_year
    district = st.session_state.booth_selected_district
    constituency = st.session_state.booth_selected_constituency
    
    render_breadcrumb([f"{year} Election", district, constituency])
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Change Selection", key="booth_back_to_dropdown"):
            st.session_state.booth_selected_district = None
            st.session_state.booth_selected_constituency = None
            st.rerun()
    
    booth_data = booth_df[(booth_df['year'] == year) &
                          (booth_df['district'] == district) &
                          (booth_df['constituency'] == constituency)]
    
    unique_booths = booth_data[['booth_id', 'booth_name', 'total_voters', 'votes_polled',
                                 'previous_error', 'postal_votes', 'tendered_votes']].drop_duplicates()
    
    booth_winners = booth_data[booth_data['winner'] == 'Yes'][['booth_id', 'candidate', 'party', 'margin']]
    
    booth_summary = unique_booths.merge(booth_winners, on='booth_id', how='left')
    booth_summary['turnout_percentage'] = (booth_summary['votes_polled'] / booth_summary['total_voters'] * 100).round(1)
    
    tab1, tab2, tab3 = st.tabs(["📋 Booth List", "🔍 Booth Details", "📊 Polling Analysis"])
    
    with tab1:
        st.markdown(f"##### Booths in {constituency}")
        
        display_cols = ['booth_id', 'booth_name', 'total_voters', 'votes_polled', 'turnout_percentage',
                       'candidate', 'party', 'margin']
        display_df = booth_summary[display_cols].copy()
        
        display_df['turnout_percentage'] = display_df['turnout_percentage'].astype(str) + '%'
        display_df['margin'] = display_df['margin'].astype(str) + ' votes'
        
        display_df.columns = ['Booth ID', 'Booth Name', 'Total Voters', 'Votes Polled',
                             'Turnout %', 'Winner', 'Party', 'Margin']
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        st.info(f"Showing {len(display_df)} booths in {constituency}")
    
    with tab2:
        st.markdown("##### Booth Details")
        
        if not booth_summary.empty:
            booth_options = booth_summary.apply(lambda x: f"{x['booth_id']} - {x['booth_name']}", axis=1).tolist()
            selected_booth = st.selectbox("Select a Booth", booth_options, key="booth_detail_select")
            
            booth_id = int(selected_booth.split(' - ')[0])
            booth_detail = booth_summary[booth_summary['booth_id'] == booth_id].iloc[0]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(f'''
                <div class="stat-box">
                    <div class="stat-icon">🏛️</div>
                    <div class="stat-label">Booth ID</div>
                    <div class="stat-value">{booth_detail['booth_id']}</div>
                </div>
                ''', unsafe_allow_html=True)
                st.markdown(f'''
                <div class="stat-box" style="margin-top: 1rem;">
                    <div class="stat-label">Total Voters</div>
                    <div class="stat-value">{booth_detail['total_voters']:,}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col2:
                st.markdown(f'''
                <div class="stat-box">
                    <div class="stat-icon">🗳️</div>
                    <div class="stat-label">Votes Polled</div>
                    <div class="stat-value">{booth_detail['votes_polled']:,}</div>
                </div>
                ''', unsafe_allow_html=True)
                st.markdown(f'''
                <div class="stat-box" style="margin-top: 1rem;">
                    <div class="stat-label">Turnout</div>
                    <div class="stat-value">{booth_detail['turnout_percentage']}%</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col3:
                st.markdown(f'''
                <div class="stat-box">
                    <div class="stat-icon">🏆</div>
                    <div class="stat-label">Winner</div>
                    <div class="stat-value" style="font-size: 1.1rem;">{booth_detail['candidate']}</div>
                    <div class="stat-sublabel">{booth_detail['party']}</div>
                </div>
                ''', unsafe_allow_html=True)
                st.markdown(f'''
                <div class="stat-box" style="margin-top: 1rem;">
                    <div class="stat-label">Margin</div>
                    <div class="stat-value">{booth_detail['margin']}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
            
            booth_candidates = booth_data[booth_data['booth_id'] == booth_id]
            
            st.markdown("##### Candidate-wise Vote Split")
            
            candidates_df = booth_candidates[['candidate', 'party', 'votes']].copy()
            total_booth_votes = booth_candidates['votes'].sum()
            candidates_df['Percentage'] = (candidates_df['votes'] / total_booth_votes * 100).round(1).astype(str) + '%'
            
            col1, col2 = st.columns([1, 1])
            with col1:
                st.dataframe(candidates_df, use_container_width=True, hide_index=True)
            
            with col2:
                fig = px.pie(candidates_df, values='votes', names='candidate',
                             color_discrete_sequence=['#234d3c', '#2d6a4f', '#40916c', '#52b788'])
                fig.update_traces(textposition='inside', textinfo='percent+label')
                fig.update_layout(showlegend=False, margin=dict(t=20, b=20, l=20, r=20))
                st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        st.markdown("##### Polling Analysis")
        
        if not booth_summary.empty:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                avg_turnout = booth_summary['turnout_percentage'].mean()
                st.markdown(f'''
                <div class="metric-card">
                    <div class="label">Avg Turnout</div>
                    <div class="value">{avg_turnout:.1f}%</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col2:
                total_voters = booth_summary['total_voters'].sum()
                st.markdown(f'''
                <div class="metric-card">
                    <div class="label">Total Voters</div>
                    <div class="value">{total_voters:,}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col3:
                total_votes = booth_summary['votes_polled'].sum()
                st.markdown(f'''
                <div class="metric-card">
                    <div class="label">Total Votes</div>
                    <div class="value">{total_votes:,}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            with col4:
                total_postal = booth_summary['postal_votes'].sum()
                st.markdown(f'''
                <div class="metric-card">
                    <div class="label">Postal Votes</div>
                    <div class="value">{total_postal}</div>
                </div>
                ''', unsafe_allow_html=True)
            
            st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
            st.markdown("##### Turnout Comparison Across Booths")
            
            turnout_chart = booth_summary[['booth_id', 'turnout_percentage']].copy()
            turnout_chart['booth_id'] = turnout_chart['booth_id'].astype(str)
            
            fig = px.bar(turnout_chart, x='booth_id', y='turnout_percentage',
                        color_discrete_sequence=['#234d3c'])
            fig.update_layout(
                xaxis_title="Booth ID",
                yaxis_title="Turnout %",
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)

render_footer()
