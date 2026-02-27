import streamlit as st
import pandas as pd
from pathlib import Path

# Get the base directory (where utils.py is located)
BASE_DIR = Path(__file__).parent

def setup_page(page_title="Pollytics"):
    """Sets up the standard page layout, title, logo, and custom CSS."""
    st.set_page_config(page_title=page_title, layout="wide")
    
    # Load custom CSS
    css_path = BASE_DIR / "assets" / "style.css"
    try:
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Failed to load custom CSS: {e}")

    # Create columns for logo and title
    col1, col2, col3 = st.columns([1, 10, 1])

    with col1:
        # Display logo using st.image
        logo_path = BASE_DIR / "assets" / "ECK_LOGO.jpg"
        try:
            st.image(str(logo_path), width=70)
        except Exception:
            st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Election_Commission_of_India_logo.png/120px-Election_Commission_of_India_logo.png", width=70)

    with col2:
        # Title in the middle
        st.markdown("""
        <div class="kerala-header" style="margin-top: -20px;">
            <h1>🗳️ POLLYTICS</h1>
            <p>KERALA ELECTION ANALYSIS PORTAL</p>
            <div class="malayalam">കേരള തിരഞ്ഞെടുപ്പ് വിശകലന കേന്ദ്രം</div>
        </div>
        """, unsafe_allow_html=True)

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
    # All 14 districts of Kerala
    districts = [
        'Thiruvananthapuram', 'Kollam', 'Pathanamthitta', 'Alappuzha', 'Kottayam',
        'Idukki', 'Ernakulam', 'Thrissur', 'Palakkad', 'Malappuram',
        'Kozhikode', 'Wayanad', 'Kannur', 'Kasaragod'
    ]
    
    # Major constituencies in each district
    constituencies = {
        'Thiruvananthapuram': ['Vattiyoorkavu', 'Nemom', 'Kazhakoottom', 'Kovalam', 'Parassala'],
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
        'year': [],
        'district': [],
        'constituency': [],
        'booth_id': [],
        'booth_name': [],
        'total_voters': [],
        'votes_polled': [],
        'candidate': [],
        'party': [],
        'votes': [],
        'winner': [],
        'margin': [],
        'previous_error': [],
        'postal_votes': [],
        'tendered_votes': []
    }
    
    # Generate data for each district, constituency, and booth
    booth_counter = 1
    parties = ['CPI', 'INC', 'BJP', 'CPIM', 'IUML', 'KC(M)', 'JD(S)']
    candidates = ['Suresh', 'Rajan', 'Meera', 'Anand', 'Priya', 'Manoj', 'Deepa',
                  'Sunil', 'Bindu', 'Vijayan', 'Uma', 'George', 'Jose', 'Peter']
    
    for year in [2023, 2024, 2025]:
        for district in districts:
            district_constituencies = constituencies[district]
            # 10 booths per constituency
            for i in range(10):
                const_index = i % len(district_constituencies)
                constituency = district_constituencies[const_index]
                
                # Generate booth data
                total = 1200 + (i * 50) + (hash(f"{district}_{i}") % 300)
                turnout = 65 + (i * 2) + (hash(constituency) % 15)
                if turnout > 90:
                    turnout = 90
                votes_polled = int(total * turnout / 100)
                
                # Generate candidate data (3-4 candidates per booth)
                num_candidates = 3 + (hash(f"cand_{booth_counter}") % 2)
                remaining_votes = votes_polled
                
                # Determine winner (gets ~40-60% of votes)
                winner_idx = (booth_counter + i) % len(candidates)
                winner_name = candidates[winner_idx]
                winner_party = parties[(winner_idx + hash(constituency)) % len(parties)]
                winner_votes = int(votes_polled * (0.4 + (hash(f"win_{booth_counter}") % 20)/100))
                
                # Calculate margin (winner - runner up)
                runner_up_votes = int((votes_polled - winner_votes) * 0.6)
                margin = winner_votes - runner_up_votes
                
                for j in range(num_candidates):
                    if j == 0:  # Winner
                        candidate_name = winner_name
                        party = winner_party
                        vote_count = winner_votes
                        is_winner = 'Yes'
                        booth_margin = margin
                    else:
                        # Other candidates
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
                    
                    # Add candidate data
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
