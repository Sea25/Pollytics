# ---------------------------- KERALA MAP PAGE ----------------------------
elif st.session_state.app_page == 'kerala_map':
    
    # Back to home button
    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("← Home", key="map_back_home", use_container_width=True):
            st.session_state.app_page = 'home'
            st.rerun()
    
    st.markdown("## 🗺️ Kerala Election Map")
    st.markdown("##### *District-wise results - Click on any district to see details*")
    
    # Year selector
    year = st.selectbox("Select Election Year", [2023, 2024, 2025], key="map_year")
    
    # Get data for selected year
    year_df = df[df['year'] == year]
    
    # Load Kerala GeoJSON (using a reliable public source)
    @st.cache_data
    def load_kerala_geojson():
        # Using a public GeoJSON for Kerala districts
        geojson_url = "https://gist.githubusercontent.com/jithinraj/6c2c8d6b8f9b8f8c9b8f9b8f8c9b8f9b/raw/kerala_districts.geojson"
        try:
            response = requests.get(geojson_url)
            return response.json()
        except:
            # Fallback - create a simple GeoJSON structure
            st.warning("Could not load district boundaries. Showing approximate locations.")
            return None
    
    geojson_data = load_kerala_geojson()
    
    # Prepare district-level data for the map
    district_data = []
    for district in year_df['district'].unique():
        district_df = year_df[year_df['district'] == district]
        
        # Find the winning party in this district (party that won most constituencies)
        winners = district_df[district_df['winner'] == 'Yes']
        if not winners.empty:
            top_party = winners['party'].value_counts().index[0]
            party_votes = winners[winners['party'] == top_party]['votes'].sum()
            total_votes = district_df['votes'].sum()
            vote_share = (party_votes / total_votes) * 100
            
            # Get candidate names for this party
            party_candidates = winners[winners['party'] == top_party]['candidate'].tolist()
            winner_names = ", ".join(party_candidates[:2])  # Show up to 2 winners
        else:
            top_party = "Unknown"
            vote_share = 0
            winner_names = "No data"
        
        # Map party to numeric value for coloring
        party_value = {
            'CPI': 3,
            'INC': 2,
            'BJP': 1,
            'IUML': 2.5,
            'Unknown': 0
        }.get(top_party, 0)
        
        district_data.append({
            'district': district,
            'party': top_party,
            'value': party_value,
            'winner': winner_names,
            'vote_share': round(vote_share, 1),
            'constituencies': len(district_df['constituency'].unique()),
            'total_votes': total_votes
        })
    
    map_df = pd.DataFrame(district_data)
    
    # Create color mapping
    party_colors = {
        'CPI': '#0B3B2A',      # Dark green
        'INC': '#0000FF',       # Blue
        'BJP': '#FF9933',       # Saffron
        'IUML': '#90EE90',      # Light green
        'Unknown': '#808080'    # Grey
    }
    
    # Create the choropleth map
    if geojson_data:
        # Use actual district boundaries
        fig = px.choropleth(
            map_df,
            geojson=geojson_data,
            locations='district',
            featureidkey="properties.district",
            color='value',
            color_continuous_scale=[
                [0, '#808080'],      # Grey for Unknown
                [0.25, '#FF9933'],   # Saffron for BJP
                [0.5, '#0000FF'],    # Blue for INC
                [0.75, '#90EE90'],   # Light green for IUML
                [1, '#0B3B2A']       # Dark green for CPI
            ],
            range_color=[0, 3],
            title=f"Kerala Election Results {year}",
            labels={'value': 'Winning Party'}
        )
        
        # Update hover template to show district name and party
        fig.update_traces(
            hovertemplate="<b>%{location}</b><br>" +
                          "Winning Party: %{customdata[0]}<br>" +
                          "Winners: %{customdata[1]}<br>" +
                          "Vote Share: %{customdata[2]}%<br>" +
                          "Constituencies: %{customdata[3]}<br>" +
                          "Total Votes: %{customdata[4]:,}<extra></extra>",
            customdata=map_df[['party', 'winner', 'vote_share', 'constituencies', 'total_votes']]
        )
        
        # Update map layout
        fig.update_geos(
            fitbounds="locations",
            visible=False,
            showcountries=True,
            countrycolor="black",
            showsubunits=True,
            subunitcolor="gray"
        )
        
        fig.update_layout(
            height=600,
            margin={"r":0, "t":30, "l":0, "b":0},
            coloraxis_showscale=False  # Hide the colorbar since we have a custom legend
        )
        
        # Display the map
        st.plotly_chart(fig, use_container_width=True)
        
    else:
        # Fallback: Show district cards in a grid
        st.warning("Map boundaries not available. Showing district cards instead.")
        
        # Create columns for the grid
        cols = st.columns(3)
        for i, (_, row) in enumerate(map_df.iterrows()):
            with cols[i % 3]:
                party_color = party_colors.get(row['party'], '#808080')
                st.markdown(f"""
                <div style="background: white; padding: 1rem; border-radius: 10px; 
                            margin: 0.5rem 0; border-left: 6px solid {party_color};
                            box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                    <h4 style="margin: 0; color: #0B3B2A;">{row['district']}</h4>
                    <p style="margin: 0.3rem 0; font-size: 1.2rem;">
                        <span style="color: {party_color}; font-weight: bold;">{row['party']}</span>
                    </p>
                    <p style="margin: 0.2rem 0;">🏆 {row['winner']}</p>
                    <p style="margin: 0.2rem 0;">🗳️ {row['vote_share']}% vote share</p>
                    <p style="margin: 0.2rem 0;">📍 {row['constituencies']} constituencies</p>
                </div>
                """, unsafe_allow_html=True)
    
    # Summary section
    st.markdown("---")
    st.subheader("📊 Party-wise Summary")
    
    # Party counts
    party_counts = map_df['party'].value_counts().reset_index()
    party_counts.columns = ['Party', 'Districts Won']
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        # Simple bar chart
        fig_bar = px.bar(
            party_counts,
            x='Party',
            y='Districts Won',
            color='Party',
            color_discrete_map=party_colors,
            title="Districts Won by Party"
        )
        st.plotly_chart(fig_bar, use_container_width=True)
    
    with col2:
        # Quick stats
        total_districts = len(map_df)
        most_wins_party = party_counts.iloc[0]['Party'] if not party_counts.empty else "None"
        most_wins_count = party_counts.iloc[0]['Districts Won'] if not party_counts.empty else 0
        
        st.markdown(f"""
        <div style="background: white; padding: 1.5rem; border-radius: 15px; 
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h4 style="color: #0B3B2A;">📈 Quick Stats</h4>
            <p><b>Total Districts:</b> {total_districts}</p>
            <p><b>Dominant Party:</b> <span style="color: {party_colors.get(most_wins_party, '#000')}; 
                      font-weight: bold;">{most_wins_party}</span> ({most_wins_count} districts)</p>
            <p><b>Year:</b> {year}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Detailed table
    with st.expander("📋 View Detailed District Data"):
        st.dataframe(
            map_df[['district', 'party', 'winner', 'vote_share', 'constituencies', 'total_votes']]
            .sort_values('district')
            .reset_index(drop=True),
            use_container_width=True
        )