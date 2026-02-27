import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="Kerala Election Portal",
    page_icon="🗳️",
    layout="wide"
)

# Initialize language state for content ONLY
if 'content_lang' not in st.session_state:
    st.session_state.content_lang = "English"  # Default

# Kerala-style header (ALWAYS bilingual - NO CHANGE)
st.markdown("""
<div style="
    background: linear-gradient(90deg, #1B4D3E 0%, #2E7D32 100%);
    padding: 2rem;
    border-radius: 5px;
    margin-bottom: 2rem;
    text-align: center;
">
    <h1 style="color: white; margin: 0;">🗳️ കേരള തിരഞ്ഞെടുപ്പ് വിശകലനം</h1>
    <p style="color: #FFD700; font-size: 1.2rem;">Kerala Election Analytics Portal</p>
</div>
""", unsafe_allow_html=True)

# Load sample data
@st.cache_data
def load_data():
    df = pd.read_csv('data/sample_data.csv')
    return df

df = load_data()

# Translation dictionaries
candidate_translation = {
    "Suresh": "സുരേഷ്",
    "Rajan": "രാജൻ", 
    "Meera": "മീര",
    "Anand": "ആനന്ദ്"
}

party_translation = {
    "CPI": "സി.പി.ഐ",
    "INC": "ഐ.എൻ.സി"
}

constituency_translation = {
    "Trivandrum": "തിരുവനന്തപുരം",
    "Kochi": "കൊച്ചി"
}

# Function to translate dataframe
def translate_df(df, lang):
    if lang == "English":
        return df
    
    df_translated = df.copy()
    df_translated['candidate'] = df['candidate'].map(candidate_translation).fillna(df['candidate'])
    df_translated['party'] = df['party'].map(party_translation).fillna(df['party'])
    df_translated['constituency'] = df['constituency'].map(constituency_translation).fillna(df['constituency'])
    return df_translated

# Sidebar 
st.sidebar.title("Navigation")

# Language toggle button for content ONLY
if st.sidebar.button("🌐 മലയാളം" if st.session_state.content_lang == "English" else "🌐 English"):
    if st.session_state.content_lang == "English":
        st.session_state.content_lang = "Malayalam"
    else:
        st.session_state.content_lang = "English"
    st.rerun()

# Page navigation (dynamic based on language)
page_labels = ["Home", "Results", "Booth Analysis"]
ml_page_labels = ["ഹോം", "ഫലങ്ങൾ", "ബൂത്ത് വിശകലനം"]

if st.session_state.content_lang == "English":
    page = st.sidebar.radio("Go to", page_labels)
else:
    page = st.sidebar.radio("പേജ് തിരഞ്ഞെടുക്കുക", ml_page_labels)
    # Map back to English page names for logic
    page_map = dict(zip(ml_page_labels, page_labels))
    page = page_map[page]

# Dictionary for UI labels
ml_labels = {
    "Home": {
        "title": "വെൽക്കം ടു കേരള ഇലക്ഷൻ അനലിറ്റിക്സ്",
        "desc": "ഈ പോർട്ടൽ തിരഞ്ഞെടുപ്പ് ഫലങ്ങളുടെ വിശദമായ വിശകലനം നൽകുന്നു.",
        "total_const": "ആകെ മണ്ഡലങ്ങൾ",
        "total_cand": "ആകെ സ്ഥാനാർത്ഥികൾ", 
        "total_votes": "ആകെ വോട്ടുകൾ"
    },
    "Results": {
        "title": "തിരഞ്ഞെടുപ്പ് ഫലങ്ങൾ",
        "select_const": "മണ്ഡലം തിരഞ്ഞെടുക്കുക",
        "vote_dist": "വോട്ട് വിതരണം - "
    },
    "Booth": {
        "title": "ബൂത്ത് തല വിശകലനം",
        "enter_booth": "ബൂത്ത് ഐഡി നൽകുക",
        "winner": "ബൂത്ത് {0} ലെ വിജയി: {1}",
        "not_found": "ബൂത്ത് ഐഡി കണ്ടെത്തിയില്ല"
    },
    "columns": {
        "candidate": "സ്ഥാനാർത്ഥി",
        "party": "പാർട്ടി", 
        "votes": "വോട്ടുകൾ",
        "booth_id": "ബൂത്ത് നമ്പർ",
        "winner": "വിജയി",
        "constituency": "മണ്ഡലം"
    }
}

# Translate data if in Malayalam mode
if st.session_state.content_lang == "Malayalam":
    display_df = translate_df(df, "Malayalam")
else:
    display_df = df.copy()

# Display content based on language
if page == "Home":
    if st.session_state.content_lang == "English":
        st.header("Welcome to Kerala Election Analytics")
        st.write("This portal provides detailed analysis of election results.")
        
        # Show quick stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Constituencies", df['constituency'].nunique())
        with col2:
            st.metric("Total Candidates", df['candidate'].nunique())
        with col3:
            st.metric("Total Votes", f"{df['votes'].sum():,}")
    else:
        st.header(ml_labels["Home"]["title"])
        st.write(ml_labels["Home"]["desc"])
        
        # Show quick stats in Malayalam
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric(ml_labels["Home"]["total_const"], display_df['constituency'].nunique())
        with col2:
            st.metric(ml_labels["Home"]["total_cand"], display_df['candidate'].nunique())
        with col3:
            st.metric(ml_labels["Home"]["total_votes"], f"{display_df['votes'].sum():,}")

elif page == "Results":
    if st.session_state.content_lang == "English":
        st.header("Election Results")
        constituency = st.selectbox("Select Constituency", df['constituency'].unique())
        filtered_df = df[df['constituency'] == constituency]
    else:
        st.header(ml_labels["Results"]["title"])
        constituency_options = display_df['constituency'].unique()
        constituency = st.selectbox(ml_labels["Results"]["select_const"], constituency_options)
        # Get original constituency name for filtering
        reverse_const_map = {v: k for k, v in constituency_translation.items()}
        original_const = reverse_const_map.get(constituency, constituency)
        filtered_df = df[df['constituency'] == original_const]
        
        # Translate the filtered df for display
        filtered_df_display = translate_df(filtered_df, "Malayalam")
    
    # For English display
    if st.session_state.content_lang == "English":
        display_results = filtered_df
        # Rename columns for display
        display_results = display_results.rename(columns={
            'candidate': 'Candidate',
            'party': 'Party',
            'votes': 'Votes',
            'booth_id': 'Booth ID',
            'winner': 'Winner'
        })
    else:
        display_results = filtered_df_display
        # Rename columns to Malayalam
        display_results = display_results.rename(columns=ml_labels["columns"])
    
    st.dataframe(display_results)
    
    # Chart
    chart_title = f"Vote Distribution - {constituency}" if st.session_state.content_lang == "English" else f"{ml_labels['Results']['vote_dist']} {constituency}"
    fig = px.bar(filtered_df, x='candidate', y='votes', color='party', 
                 title=chart_title)
    
    # Update chart labels if Malayalam
    if st.session_state.content_lang == "Malayalam":
        fig.update_xaxes(title_text="സ്ഥാനാർത്ഥി")
        fig.update_yaxes(title_text="വോട്ടുകൾ")
    
    st.plotly_chart(fig)

elif page == "Booth Analysis":
    if st.session_state.content_lang == "English":
        st.header("Booth Level Analysis")
        booth_id = st.text_input("Enter Booth ID (e.g., 101)")
    else:
        st.header(ml_labels["Booth"]["title"])
        booth_id = st.text_input(ml_labels["Booth"]["enter_booth"])
    
    if booth_id:
        booth_df = df[df['booth_id'] == int(booth_id)]
        if not booth_df.empty:
            if st.session_state.content_lang == "English":
                display_booth = booth_df.rename(columns={
                    'candidate': 'Candidate',
                    'party': 'Party',
                    'votes': 'Votes',
                    'booth_id': 'Booth ID',
                    'winner': 'Winner'
                })
                st.dataframe(display_booth)
                winner = booth_df[booth_df['winner'] == 'Yes']['candidate'].values[0]
                st.success(f"Winner in Booth {booth_id}: {winner}")
            else:
                # Translate booth data
                booth_df_display = translate_df(booth_df, "Malayalam")
                booth_df_display = booth_df_display.rename(columns=ml_labels["columns"])
                st.dataframe(booth_df_display)
                winner = booth_df[booth_df['winner'] == 'Yes']['candidate'].values[0]
                winner_ml = candidate_translation.get(winner, winner)
                st.success(ml_labels["Booth"]["winner"].format(booth_id, winner_ml))
        else:
            if st.session_state.content_lang == "English":
                st.error("Booth ID not found")
            else:
                st.error(ml_labels["Booth"]["not_found"])

st.sidebar.markdown("---")
st.sidebar.info("tinkHerHack 4.0 | Team Checkmate")
