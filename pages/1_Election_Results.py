import streamlit as st
import pandas as pd
import plotly.express as px
from utils import setup_page, load_data, render_page_header, render_breadcrumb, render_footer

setup_page("Election Results - Pollytics")

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("← Home", key="results_back_home", use_container_width=True):
        st.session_state.selected_year = None
        st.session_state.selected_district = None
        st.session_state.selected_constituency = None
        st.switch_page("app.py")

render_page_header("Election Results", "Explore constituency-wise election results with detailed analysis", "📊")

df = load_data()

if 'selected_year' not in st.session_state:
    st.session_state.selected_year = None
if 'selected_district' not in st.session_state:
    st.session_state.selected_district = None
if 'selected_constituency' not in st.session_state:
    st.session_state.selected_constituency = None

if st.session_state.selected_year is None:
    st.markdown("""
    <p style="color: #6b7280; margin-bottom: 1.5rem;">Select an election year to begin exploring the results.</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="year-box"><h2>2023</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
        if st.button("Select 2023", key="e_2023", use_container_width=True, type="primary"):
            st.session_state.selected_year = 2023
            st.rerun()
    
    with col2:
        st.markdown('<div class="year-box"><h2>2024</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
        if st.button("Select 2024", key="e_2024", use_container_width=True, type="primary"):
            st.session_state.selected_year = 2024
            st.rerun()
    
    with col3:
        st.markdown('<div class="year-box"><h2>2025</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
        if st.button("Select 2025", key="e_2025", use_container_width=True, type="primary"):
            st.session_state.selected_year = 2025
            st.rerun()

elif st.session_state.selected_constituency is None:
    render_breadcrumb([f"{st.session_state.selected_year} Election", "Select Location"])
    
    if st.button("← Change Year", key="back_to_year"):
        st.session_state.selected_year = None
        st.rerun()
    
    year_df = df[df['year'] == st.session_state.selected_year]
    
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
            key="district_dropdown",
            format_func=lambda x: "Choose a district..." if x == "" else x
        )
    
    with col2:
        if selected_district and selected_district != "":
            constituencies = sorted(year_df[year_df['district'] == selected_district]['constituency'].unique())
            selected_constituency = st.selectbox(
                "Constituency",
                options=[""] + list(constituencies),
                key="constituency_dropdown",
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
            if st.button("View Results", use_container_width=True, type="primary"):
                st.session_state.selected_district = selected_district
                st.session_state.selected_constituency = selected_constituency
                st.rerun()

else:
    year = st.session_state.selected_year
    district = st.session_state.selected_district
    constituency = st.session_state.selected_constituency
    
    render_breadcrumb([f"{year} Election", district, constituency])
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Change Selection", key="back_to_dropdown"):
            st.session_state.selected_district = None
            st.session_state.selected_constituency = None
            st.rerun()
    
    const_data = df[(df['year'] == year) &
                    (df['district'] == district) &
                    (df['constituency'] == constituency)].copy()
    
    if not const_data.empty:
        winner = const_data[const_data['winner'] == 'Yes'].iloc[0]
        runner_up = const_data[const_data['winner'] == 'No'].sort_values('votes', ascending=False).iloc[0]
        
        st.markdown(f"""
        <div class="winner-card">
            <h2>🏆 WINNER</h2>
            <div class="candidate-name">{winner['candidate']}</div>
            <div class="party">{winner['party']}</div>
            <div class="votes">{winner['votes']:,} Votes</div>
        </div>
        """, unsafe_allow_html=True)
        
        total_votes = const_data['votes'].sum()
        margin = winner['votes'] - runner_up['votes']
        vote_share = (winner['votes'] / total_votes) * 100
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <div class="label">Total Votes</div>
                <div class="value">{total_votes:,}</div>
            </div>
            ''', unsafe_allow_html=True)
        with col2:
            st.markdown(f'''
            <div class="metric-card">
                <div class="label">Winning Margin</div>
                <div class="value">{margin:,}</div>
            </div>
            ''', unsafe_allow_html=True)
        with col3:
            st.markdown(f'''
            <div class="metric-card">
                <div class="label">Vote Share</div>
                <div class="value">{vote_share:.1f}%</div>
            </div>
            ''', unsafe_allow_html=True)
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <div class="label">Runner Up</div>
                <div class="value" style="font-size: 1.1rem;">{runner_up["candidate"]}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("##### Vote Distribution")
            fig = px.bar(
                const_data.sort_values('votes', ascending=False),
                x='candidate',
                y='votes',
                color='party',
                color_discrete_map={'CPI': '#234d3c', 'INC': '#3b82f6', 'BJP': '#f97316', 'CPIM': '#dc2626', 'IUML': '#22c55e'}
            )
            fig.update_layout(
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                margin=dict(t=30, b=30, l=30, r=30),
                xaxis_title="",
                yaxis_title="Votes",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("##### Vote Share")
            fig = px.pie(
                const_data,
                values='votes',
                names='candidate',
                color_discrete_sequence=['#234d3c', '#2d6a4f', '#40916c', '#52b788', '#74c69d']
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(
                showlegend=False,
                margin=dict(t=30, b=30, l=30, r=30)
            )
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown(f"##### Other Constituencies in {district} District")
        
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
                        <div class="winner">🏆 {row['candidate']} ({row['party']}) • {row['votes']:,} votes</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with st.expander("📋 View Detailed Results Table"):
            st.dataframe(
                const_data[['candidate', 'party', 'votes']]
                .sort_values('votes', ascending=False)
                .reset_index(drop=True),
                use_container_width=True
            )
    else:
        st.error("No data found for this selection")

render_footer()
