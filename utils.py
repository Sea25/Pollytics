import streamlit as st
import pandas as pd
from pathlib import Path
import base64

BASE_DIR = Path(__file__).parent

def get_logo_base64():
    """Get logo as base64 string for embedding in HTML."""
    logo_path = BASE_DIR / "assets" / "ECK_LOGO.jpg"
    try:
        with open(logo_path, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except Exception:
        return None

def setup_page(page_title="Pollytics"):
    """Sets up the standard page layout with fixed header and logo."""
    st.set_page_config(
        page_title=page_title, 
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    css_path = BASE_DIR / "assets" / "style.css"
    try:
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Failed to load custom CSS: {e}")
    
    logo_b64 = get_logo_base64()
    
    if logo_b64:
        logo_html = f'<img src="data:image/jpeg;base64,{logo_b64}" alt="Pollytics Logo" style="width: 42px; height: 42px; object-fit: contain;">'
    else:
        logo_html = '''<svg width="42" height="42" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="100" height="100" rx="12" fill="#234d3c"/>
            <path d="M25 70V30h15v40H25zm17.5-25V30H60v15H42.5zm0 25V55H60v15H42.5zM62.5 70V30H75v40H62.5z" fill="#d4a03c"/>
        </svg>'''
    
    st.markdown(f'''
    <div class="site-header">
        <div class="logo-container">
            {logo_html}
        </div>
        <div class="brand">
            <div class="brand-name">POLLYTICS</div>
            <div class="brand-tagline">Kerala Election Analysis Portal</div>
        </div>
    </div>
    <div class="header-spacer"></div>
    ''', unsafe_allow_html=True)

def render_page_header(title, subtitle=None, icon=None):
    """Render a consistent page header."""
    icon_html = f'<span style="font-size: 1.5rem;">{icon}</span>' if icon else ''
    subtitle_html = f'<p class="page-subtitle">{subtitle}</p>' if subtitle else ''
    
    st.markdown(f'''
    <div style="margin-bottom: 1.5rem;">
        <h1 class="page-title">{icon_html} {title}</h1>
        {subtitle_html}
    </div>
    ''', unsafe_allow_html=True)

def render_breadcrumb(items):
    """Render a breadcrumb navigation."""
    breadcrumb_items = []
    for i, item in enumerate(items):
        if i == len(items) - 1:
            breadcrumb_items.append(f'<span class="current">{item}</span>')
        else:
            breadcrumb_items.append(f'<span>{item}</span>')
    
    st.markdown(f'''
    <div class="breadcrumb">
        {' <span class="separator">→</span> '.join(breadcrumb_items)}
    </div>
    ''', unsafe_allow_html=True)

def render_filter_section(title=None):
    """Start a filter section container."""
    title_html = f'<div class="filter-section-title">{title}</div>' if title else ''
    return f'''
    <div class="filter-section">
        {title_html}
    '''

def render_footer():
    """Render the site footer."""
    st.markdown('''
    <div class="site-footer">
        <p><span class="highlight">POLLYTICS</span> - Kerala Election Analysis Portal</p>
        <p style="font-size: 0.75rem; opacity: 0.7; margin-top: 0.5rem;">© 2025 Pollytics. Data sourced from Election Commission of Kerala.</p>
    </div>
    ''', unsafe_allow_html=True)

@st.cache_data
def load_data():
    """Load Kerala election data from CSV."""
    try:
        data_path = BASE_DIR / "data" / "kerala_election_data.csv"
        df = pd.read_csv(data_path)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.info("Please make sure the file 'data/kerala_election_data.csv' exists in the data folder")
        return pd.DataFrame()

@st.cache_data
def create_booth_data():
    """Create sample data with all 14 districts of Kerala and 10 booths each."""
    districts = [
        'Thiruvananthapuram', 'Kollam', 'Pathanamthitta', 'Alappuzha', 'Kottayam',
        'Idukki', 'Ernakulam', 'Thrissur', 'Palakkad', 'Malappuram',
        'Kozhikode', 'Wayanad', 'Kannur', 'Kasaragod'
    ]
    
    constituencies = {
        'Thiruvananthapuram': ['Vattiyoorkavu', 'Nemom', 'Kazhakoottam', 'Kovalam', 'Parassala'],
        'Kollam': ['Kollam', 'Kundara', 'Chavara', 'Punalur', 'Karunagappally'],
        'Pathanamthitta': ['Pathanamthitta', 'Ranni', 'Aranmula', 'Konni', 'Adoor'],
        'Alappuzha': ['Alappuzha', 'Cherthala', 'Ambalappuzha', 'Haripad', 'Kayamkulam'],
        'Kottayam': ['Kottayam', 'Changanassery', 'Pala', 'Vaikom', 'Kaduthuruthy'],
        'Idukki': ['Idukki', 'Peerumade', 'Udumbanchola', 'Devikulam', 'Thodupuzha'],
        'Ernakulam': ['Ernakulam', 'Thrikkakara', 'Kalamassery', 'Paravur', 'Aluva'],
        'Thrissur': ['Thrissur', 'Ollur', 'Irinjalakuda', 'Guruvayur', 'Kodungallur'],
        'Palakkad': ['Palakkad', 'Ottapalam', 'Mannarkkad', 'Chittur', 'Alathur'],
        'Malappuram': ['Malappuram', 'Manjeri', 'Ponnani', 'Tirur', 'Perinthalmanna'],
        'Kozhikode': ['Kozhikode North', 'Kozhikode South', 'Beypore', 'Kunnamangalam', 'Koduvally'],
        'Wayanad': ['Sulthan Bathery', 'Kalpetta', 'Mananthavady', 'Vythiri', 'Panamaram'],
        'Kannur': ['Kannur', 'Thalassery', 'Payyanur', 'Taliparamba', 'Iritty'],
        'Kasaragod': ['Kasaragod', 'Kanhangad', 'Uppala', 'Manjeshwar', 'Vellarikundu']
    }
    
    data = {
        'year': [], 'district': [], 'constituency': [], 'booth_id': [],
        'booth_name': [], 'total_voters': [], 'votes_polled': [],
        'candidate': [], 'party': [], 'votes': [], 'winner': [],
        'margin': [], 'previous_error': [], 'postal_votes': [], 'tendered_votes': []
    }
    
    booth_counter = 1
    parties = ['CPI', 'INC', 'BJP', 'CPIM', 'IUML', 'KC(M)', 'JD(S)']
    candidates = ['Suresh', 'Rajan', 'Meera', 'Anand', 'Priya', 'Manoj', 'Deepa',
                  'Sunil', 'Bindu', 'Vijayan', 'Uma', 'George', 'Jose', 'Peter']
    
    for year in [2023, 2024, 2025]:
        for district in districts:
            district_constituencies = constituencies[district]
            for i in range(10):
                const_index = i % len(district_constituencies)
                constituency = district_constituencies[const_index]
                
                total = 1200 + (i * 50) + (hash(f"{district}_{i}") % 300)
                turnout = 65 + (i * 2) + (hash(constituency) % 15)
                if turnout > 90:
                    turnout = 90
                votes_polled = int(total * turnout / 100)
                
                num_candidates = 3 + (hash(f"cand_{booth_counter}") % 2)
                remaining_votes = votes_polled
                
                winner_idx = (booth_counter + i) % len(candidates)
                winner_name = candidates[winner_idx]
                winner_party = parties[(winner_idx + hash(constituency)) % len(parties)]
                winner_votes = int(votes_polled * (0.4 + (hash(f"win_{booth_counter}") % 20)/100))
                
                runner_up_votes = int((votes_polled - winner_votes) * 0.6)
                margin = winner_votes - runner_up_votes
                
                for j in range(num_candidates):
                    if j == 0:
                        candidate_name = winner_name
                        party = winner_party
                        vote_count = winner_votes
                        is_winner = 'Yes'
                        booth_margin = margin
                    else:
                        cand_idx = (winner_idx + j + 1) % len(candidates)
                        candidate_name = candidates[cand_idx]
                        party = parties[(cand_idx + hash(constituency)) % len(parties)]
                        
                        if j == num_candidates - 1:
                            vote_count = remaining_votes - winner_votes
                        else:
                            vote_count = int((remaining_votes - winner_votes) / (num_candidates - j))
                            remaining_votes -= vote_count
                        
                        is_winner = 'No'
                        booth_margin = 0
                    
                    data['year'].append(year)
                    data['district'].append(district)
                    data['constituency'].append(constituency)
                    data['booth_id'].append(1000 + booth_counter)
                    data['booth_name'].append(f"Booth {booth_counter} - {['Govt. School', 'LP School', 'HSS', 'College', 'Community Hall'][i % 5]} {['North', 'South', 'East', 'West', 'Central'][i % 5]}")
                    data['total_voters'].append(total)
                    data['votes_polled'].append(votes_polled)
                    data['candidate'].append(candidate_name)
                    data['party'].append(party)
                    data['votes'].append(vote_count)
                    data['winner'].append(is_winner)
                    data['margin'].append(booth_margin)
                    data['previous_error'].append((hash(f"error_{booth_counter}") % 21))
                    data['postal_votes'].append(int(votes_polled * (2 + (hash(f"postal_{booth_counter}") % 6)) / 100))
                    data['tendered_votes'].append(hash(f"tender_{booth_counter}") % 6)
                
                booth_counter += 1
    
    return pd.DataFrame(data)
