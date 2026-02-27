import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
import json

st.set_page_config(layout="wide")

st.title("🗺️ Kerala Election Map")
st.markdown("*Click on any district to see who won*")

# Load your election data
@st.cache_data
def load_data():
    return pd.read_csv('data/kerala_election_data.csv')

df = load_data()

# Year selector
year = st.selectbox("Select Election Year", [2023, 2024, 2025])
year_df = df[df['year'] == year]

# Get winners by district
district_winners = []
for district in year_df['district'].unique():
    district_data = year_df[year_df['district'] == district]
    # Find the party that won most constituencies in this district
    winners = district_data[district_data['winner'] == 'Yes']
    top_party = winners['party'].value_counts().index[0] if not winners.empty else "Unknown"
    winner_name = winners[winners['party'] == top_party].iloc[0]['candidate'] if not winners.empty else "Unknown"
    total_votes = district_data['votes'].sum()
    
    district_winners.append({
        'district': district,
        'winning_party': top_party,
        'winner_name': winner_name,
        'total_votes': total_votes,
        'constituencies': len(district_data['constituency'].unique())
    })

winner_df = pd.DataFrame(district_winners)

# Color mapping for parties
party_colors = {
    'CPI': '#0B3B2A',      # Dark green
    'INC': '#0000FF',       # Blue
    'BJP': '#FF9933',       # Saffron
    'IUML': '#90EE90',      # Light green
    'Unknown': '#808080'    # Grey
}

# Create base map of Kerala
m = folium.Map(location=[10.5, 76.5], zoom_start=7)

# Add district boundaries (you'll need a GeoJSON file of Kerala districts)
# For now, we'll create a simple marker map

for _, row in winner_df.iterrows():
    # Approximate coordinates for Kerala districts (you'd want more accurate ones)
    district_coords = {
        'Thiruvananthapuram': [8.5, 76.9],
        'Kollam': [8.9, 76.6],
        'Pathanamthitta': [9.3, 76.8],
        'Alappuzha': [9.5, 76.4],
        'Kottayam': [9.6, 76.5],
        'Idukki': [9.8, 77.1],
        'Ernakulam': [10.0, 76.3],
        'Thrissur': [10.5, 76.2],
        'Palakkad': [10.8, 76.7],
        'Malappuram': [11.0, 76.1],
        'Kozhikode': [11.3, 75.8],
        'Wayanad': [11.6, 76.1],
        'Kannur': [11.9, 75.4],
        'Kasargod': [12.5, 75.0]
    }
    
    if row['district'] in district_coords:
        lat, lon = district_coords[row['district']]
        
        # Create popup HTML
        popup_html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4 style="color: #0B3B2A;">{row['district']} District</h4>
            <p><b>Winning Party:</b> <span style="color: {party_colors.get(row['winning_party'], '#000')};">{row['winning_party']}</span></p>
            <p><b>Winner:</b> {row['winner_name']}</p>
            <p><b>Total Votes:</b> {row['total_votes']:,}</p>
            <p><b>Constituencies:</b> {row['constituencies']}</p>
        </div>
        """
        
        # Add marker
        folium.Marker(
            [lat, lon],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=row['district'],
            icon=folium.Icon(color='green', icon='info-sign')
        ).add_to(m)

# Display the map
folium_static(m)

# Show data table below map
st.markdown("---")
st.subheader("📊 District-wise Summary")

# Color-code the party column
def color_party(val):
    color = party_colors.get(val, '#000000')
    return f'background-color: {color}; color: white'

styled_df = winner_df.style.applymap(color_party, subset=['winning_party'])
st.dataframe(styled_df, use_container_width=True)

# Simple pie chart of party-wise wins
st.subheader("🥧 Party-wise Performance")
party_counts = winner_df['winning_party'].value_counts()
st.bar_chart(party_counts)