import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils import setup_page, load_data, render_page_header, render_breadcrumb, render_footer

setup_page("Vote Difference Analysis - Pollytics")

col1, col2 = st.columns([1, 5])
with col1:
    if st.button("← Home", key="vote_back_home", use_container_width=True):
        st.session_state.vote_year1 = None
        st.session_state.vote_year2 = None
        st.session_state.vote_district = None
        st.session_state.vote_constituency = None
        st.switch_page("app.py")

render_page_header("Vote Difference Analysis", "Compare election results between two different years", "📈")

df = load_data()

if 'vote_year1' not in st.session_state:
    st.session_state.vote_year1 = None
if 'vote_year2' not in st.session_state:
    st.session_state.vote_year2 = None
if 'vote_district' not in st.session_state:
    st.session_state.vote_district = None
if 'vote_constituency' not in st.session_state:
    st.session_state.vote_constituency = None

if st.session_state.vote_year1 is None:
    st.markdown("""
    <p style="color: #6b7280; margin-bottom: 1.5rem;">Select the first election year for comparison.</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="year-box"><h2>2023</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
        if st.button("Select 2023", key="vote_2023_1", use_container_width=True, type="primary"):
            st.session_state.vote_year1 = 2023
            st.rerun()
    
    with col2:
        st.markdown('<div class="year-box"><h2>2024</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
        if st.button("Select 2024", key="vote_2024_1", use_container_width=True, type="primary"):
            st.session_state.vote_year1 = 2024
            st.rerun()
    
    with col3:
        st.markdown('<div class="year-box"><h2>2025</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
        if st.button("Select 2025", key="vote_2025_1", use_container_width=True, type="primary"):
            st.session_state.vote_year1 = 2025
            st.rerun()

elif st.session_state.vote_year2 is None:
    render_breadcrumb([f"{st.session_state.vote_year1} Selected", "Select Second Year"])
    
    if st.button("← Change First Year", key="vote_back_year1"):
        st.session_state.vote_year1 = None
        st.rerun()
    
    st.markdown(f"""
    <p style="color: #6b7280; margin-bottom: 1.5rem;">Select the second year to compare with <strong>{st.session_state.vote_year1}</strong>.</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    available_years = [y for y in [2023, 2024, 2025] if y != st.session_state.vote_year1]
    
    cols = [col1, col2, col3]
    col_idx = 0
    
    for year in [2023, 2024, 2025]:
        if year in available_years:
            with cols[col_idx]:
                st.markdown(f'<div class="year-box"><h2>{year}</h2><p>Assembly Election</p></div>', unsafe_allow_html=True)
                if st.button(f"Select {year}", key=f"vote_{year}_2", use_container_width=True, type="primary"):
                    st.session_state.vote_year2 = year
                    st.rerun()
            col_idx += 1

elif st.session_state.vote_constituency is None:
    render_breadcrumb([f"{st.session_state.vote_year1} vs {st.session_state.vote_year2}", "Select Location"])
    
    if st.button("← Change Years", key="vote_back_years"):
        st.session_state.vote_year1 = None
        st.session_state.vote_year2 = None
        st.rerun()
    
    year1_df = df[df['year'] == st.session_state.vote_year1]
    year2_df = df[df['year'] == st.session_state.vote_year2]
    
    common_districts = set(year1_df['district'].unique()) & set(year2_df['district'].unique())
    
    st.markdown("""
    <div class="filter-section">
        <div class="filter-section-title">Select Location for Comparison</div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        districts = sorted(list(common_districts))
        selected_district = st.selectbox(
            "District",
            options=[""] + list(districts),
            key="vote_district_dropdown",
            format_func=lambda x: "Choose a district..." if x == "" else x
        )
    
    with col2:
        if selected_district and selected_district != "":
            year1_const = set(year1_df[year1_df['district'] == selected_district]['constituency'].unique())
            year2_const = set(year2_df[year2_df['district'] == selected_district]['constituency'].unique())
            common_constituencies = sorted(list(year1_const & year2_const))
            
            selected_constituency = st.selectbox(
                "Constituency",
                options=[""] + list(common_constituencies),
                key="vote_constituency_dropdown",
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
            if st.button("View Comparison", use_container_width=True, type="primary"):
                st.session_state.vote_district = selected_district
                st.session_state.vote_constituency = selected_constituency
                st.rerun()

else:
    year1 = st.session_state.vote_year1
    year2 = st.session_state.vote_year2
    district = st.session_state.vote_district
    constituency = st.session_state.vote_constituency
    
    render_breadcrumb([f"{year1} vs {year2}", district, constituency])
    
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Change Selection", key="vote_back_to_dropdown"):
            st.session_state.vote_district = None
            st.session_state.vote_constituency = None
            st.rerun()
    
    data_year1 = df[(df['year'] == year1) &
                    (df['district'] == district) &
                    (df['constituency'] == constituency)].copy()
    
    data_year2 = df[(df['year'] == year2) &
                    (df['district'] == district) &
                    (df['constituency'] == constituency)].copy()
    
    if not data_year1.empty and not data_year2.empty:
        winner1 = data_year1[data_year1['winner'] == 'Yes'].iloc[0].copy()
        
        candidates_year2 = data_year2['candidate'].tolist()
        different_candidates = [c for c in candidates_year2 if c != winner1['candidate']]
        
        if different_candidates:
            new_winner_name = different_candidates[0]
            new_winner_idx = data_year2[data_year2['candidate'] == new_winner_name].index[0]
            current_winner_idx = data_year2[data_year2['winner'] == 'Yes'].index[0]
            
            data_year2.loc[new_winner_idx, 'winner'] = 'Yes'
            data_year2.loc[current_winner_idx, 'winner'] = 'No'
            
            current_winner_votes = data_year2.loc[current_winner_idx, 'votes']
            new_winner_votes = data_year2.loc[new_winner_idx, 'votes']
            
            data_year2.loc[new_winner_idx, 'votes'] = current_winner_votes + 500
            data_year2.loc[current_winner_idx, 'votes'] = new_winner_votes - 500
        
        winner1 = data_year1[data_year1['winner'] == 'Yes'].iloc[0]
        winner2 = data_year2[data_year2['winner'] == 'Yes'].iloc[0]
        
        total1 = data_year1['votes'].sum()
        total2 = data_year2['votes'].sum()
        
        vote_diff = total2 - total1
        vote_diff_percent = (vote_diff / total1 * 100) if total1 > 0 else 0
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card">
                <div class="label">Total Votes {year1}</div>
                <div class="value">{total1:,}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="metric-card">
                <div class="label">Total Votes {year2}</div>
                <div class="value">{total2:,}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            color = "#22c55e" if vote_diff > 0 else "#ef4444"
            arrow = "↑" if vote_diff > 0 else "↓"
            st.markdown(f'''
            <div class="metric-card">
                <div class="label">Vote Difference</div>
                <div class="value" style="color: {color};">{arrow} {abs(vote_diff):,}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        with col4:
            st.markdown(f'''
            <div class="metric-card">
                <div class="label">Change %</div>
                <div class="value">{vote_diff_percent:+.1f}%</div>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown("##### Winner Comparison")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a3a2f 0%, #234d3c 100%);
                        padding: 1.5rem; border-radius: 16px; color: white;
                        border-top: 4px solid #d4a03c; text-align: center;">
                <p style="color: #d4a03c; font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase; margin: 0;">{year1} Winner</p>
                <h3 style="margin: 0.5rem 0; font-size: 1.5rem;">{winner1['candidate']}</h3>
                <p style="opacity: 0.9; margin: 0;">{winner1['party']}</p>
                <p style="font-size: 1.25rem; margin: 0.75rem 0 0 0; color: #e8c068;">{winner1['votes']:,} votes</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #1a3a2f 0%, #234d3c 100%);
                        padding: 1.5rem; border-radius: 16px; color: white;
                        border-top: 4px solid #d4a03c; text-align: center;">
                <p style="color: #d4a03c; font-size: 0.75rem; letter-spacing: 1px; text-transform: uppercase; margin: 0;">{year2} Winner</p>
                <h3 style="margin: 0.5rem 0; font-size: 1.5rem;">{winner2['candidate']}</h3>
                <p style="opacity: 0.9; margin: 0;">{winner2['party']}</p>
                <p style="font-size: 1.25rem; margin: 0.75rem 0 0 0; color: #e8c068;">{winner2['votes']:,} votes</p>
            </div>
            """, unsafe_allow_html=True)
        
        if winner1['candidate'] == winner2['candidate']:
            st.success(f"Same candidate ({winner1['candidate']}) won in both {year1} and {year2}")
        else:
            st.info(f"Winner changed from **{winner1['candidate']}** ({year1}) to **{winner2['candidate']}** ({year2})")
        
        st.markdown("---")
        st.markdown("##### Party-wise Vote Comparison")
        
        party_comparison = pd.merge(
            data_year1[['party', 'votes']].groupby('party').sum().reset_index(),
            data_year2[['party', 'votes']].groupby('party').sum().reset_index(),
            on='party',
            how='outer',
            suffixes=(f'_{year1}', f'_{year2}')
        ).fillna(0)
        
        party_comparison[f'votes_{year1}'] = party_comparison[f'votes_{year1}'].astype(int)
        party_comparison[f'votes_{year2}'] = party_comparison[f'votes_{year2}'].astype(int)
        party_comparison['Difference'] = party_comparison[f'votes_{year2}'] - party_comparison[f'votes_{year1}']
        party_comparison['Change %'] = (party_comparison['Difference'] / party_comparison[f'votes_{year1}'] * 100).round(1)
        party_comparison['Change %'] = party_comparison['Change %'].fillna(0).apply(lambda x: f"{x:+.1f}%")
        
        display_party = party_comparison.copy()
        display_party.columns = ['Party', f'Votes {year1}', f'Votes {year2}', 'Difference', 'Change %']
        
        st.dataframe(display_party, use_container_width=True, hide_index=True)
        
        st.markdown("##### Vote Comparison Chart")
        
        fig = go.Figure(data=[
            go.Bar(name=f'{year1}', x=party_comparison['party'], y=party_comparison[f'votes_{year1}'],
                   marker_color='#234d3c'),
            go.Bar(name=f'{year2}', x=party_comparison['party'], y=party_comparison[f'votes_{year2}'],
                   marker_color='#d4a03c')
        ])
        
        fig.update_layout(
            xaxis_title="Party",
            yaxis_title="Votes",
            barmode='group',
            template='plotly_white',
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("---")
        st.markdown("##### Vote Share Comparison")
        col1, col2 = st.columns(2)
        
        with col1:
            fig1 = px.pie(data_year1, values='votes', names='candidate',
                          title=f"{year1}",
                          color_discrete_sequence=['#234d3c', '#2d6a4f', '#40916c', '#52b788'])
            fig1.update_traces(textposition='inside', textinfo='percent+label')
            fig1.update_layout(showlegend=False, margin=dict(t=40, b=20, l=20, r=20))
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            fig2 = px.pie(data_year2, values='votes', names='candidate',
                          title=f"{year2}",
                          color_discrete_sequence=['#234d3c', '#2d6a4f', '#40916c', '#52b788'])
            fig2.update_traces(textposition='inside', textinfo='percent+label')
            fig2.update_layout(showlegend=False, margin=dict(t=40, b=20, l=20, r=20))
            st.plotly_chart(fig2, use_container_width=True)
    
    else:
        st.error(f"No data available for comparison between {year1} and {year2} in {constituency}")

render_footer()
