import streamlit as st
import re
from utils import setup_page, load_data, create_booth_data
from chatbot import ElectionChatbot

setup_page("Election Chatbot - Pollytics")

df = load_data()
booth_df = create_booth_data()

if df.empty:
    st.error("Could not load election data. Please check your data file.")
    st.stop()

@st.cache_resource
def get_chatbot(_df, _booth_df):
    return ElectionChatbot(_df, _booth_df)

chatbot = get_chatbot(df, booth_df)

if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def format_response(text):
    """Convert markdown to HTML for display."""
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = text.replace('\n\n', '<br><br>')
    text = text.replace('\n', '<br>')
    return text

st.markdown("""
<style>
.chat-container {
    max-width: 550px;
    margin: 0 auto;
    font-family: 'Times New Roman', Times, serif;
}
.chat-box {
    background: white;
    border-radius: 20px;
    box-shadow: 0 8px 32px rgba(0,0,0,0.12);
    overflow: hidden;
}
.chat-header {
    background: linear-gradient(135deg, #234d3c, #2d6a4f);
    padding: 16px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.header-avatar {
    width: 48px;
    height: 48px;
    background: white;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
}
.header-text h3 {
    color: white;
    margin: 0;
    font-size: 18px;
    font-family: 'Times New Roman', Times, serif;
}
.header-status {
    color: #90EE90;
    font-size: 12px;
    margin-top: 2px;
    font-family: 'Times New Roman', Times, serif;
}
.header-status::before {
    content: "●";
    margin-right: 5px;
}
.chat-messages {
    background: #f5f7f9;
    padding: 20px;
    min-height: 320px;
    max-height: 380px;
    overflow-y: auto;
}
.msg-bot {
    display: flex;
    gap: 10px;
    margin-bottom: 16px;
}
.bot-icon {
    width: 32px;
    height: 32px;
    background: linear-gradient(135deg, #234d3c, #2d6a4f);
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 14px;
    flex-shrink: 0;
}
.bot-content {
    max-width: 85%;
}
.bot-name {
    font-size: 11px;
    color: #888;
    margin-bottom: 4px;
    font-family: 'Times New Roman', Times, serif;
}
.bot-text {
    background: white;
    padding: 12px 16px;
    border-radius: 0 16px 16px 16px;
    font-size: 14px;
    line-height: 1.5;
    color: #000;
    border: 1px solid #e8e8e8;
    font-family: 'Times New Roman', Times, serif;
}
.msg-user {
    display: flex;
    justify-content: flex-end;
    margin-bottom: 16px;
}
.user-text {
    background: linear-gradient(135deg, #234d3c, #2d6a4f);
    color: white;
    padding: 12px 16px;
    border-radius: 16px 16px 0 16px;
    font-size: 14px;
    max-width: 80%;
    font-family: 'Times New Roman', Times, serif;
}
.chat-footer {
    background: white;
    padding: 12px 20px;
    text-align: center;
    border-top: 1px solid #eee;
    font-size: 11px;
    color: #999;
    font-family: 'Times New Roman', Times, serif;
}
.chat-footer b {
    color: #234d3c;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    st.markdown("""
    <div class="chat-container">
        <div class="chat-box">
            <div class="chat-header">
                <div class="header-avatar">🤖</div>
                <div class="header-text">
                    <h3>PollyticsBot</h3>
                    <div class="header-status">Online Now</div>
                </div>
            </div>
            <div class="chat-messages">
    """, unsafe_allow_html=True)
    
    if not st.session_state.chat_history:
        st.markdown("""
            <div class="msg-bot">
                <div class="bot-icon">🤖</div>
                <div class="bot-content">
                    <div class="bot-name">PollyticsBot</div>
                    <div class="bot-text">👋 Hello! I'm your Kerala Election Assistant.<br><br>Ask me about election winners, vote counts, margins, party performance, and more!</div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="msg-user">
                    <div class="user-text">{msg["content"]}</div>
                </div>
                """, unsafe_allow_html=True)
            else:
                formatted_text = format_response(msg["content"])
                st.markdown(f"""
                <div class="msg-bot">
                    <div class="bot-icon">🤖</div>
                    <div class="bot-content">
                        <div class="bot-name">PollyticsBot</div>
                        <div class="bot-text">{formatted_text}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("""
            </div>
            <div class="chat-footer">Powered by <b>Pollytics</b> 🗳️</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    if not st.session_state.chat_history:
        st.markdown("**Try these questions:**")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("🏆 Who won in 2024?", key="q1", use_container_width=True):
                q = "Who won in Thiruvananthapuram in 2024?"
                st.session_state.chat_history.append({"role": "user", "content": q})
                resp = chatbot.process_query(q)
                st.session_state.chat_history.append({"role": "bot", "content": resp})
                st.rerun()
            if st.button("📊 Closest contest?", key="q3", use_container_width=True):
                q = "Which constituency had the closest contest in 2024?"
                st.session_state.chat_history.append({"role": "user", "content": q})
                resp = chatbot.process_query(q)
                st.session_state.chat_history.append({"role": "bot", "content": resp})
                st.rerun()
        with c2:
            if st.button("🗳️ CPI performance", key="q2", use_container_width=True):
                q = "How many seats did CPI win in 2024?"
                st.session_state.chat_history.append({"role": "user", "content": q})
                resp = chatbot.process_query(q)
                st.session_state.chat_history.append({"role": "bot", "content": resp})
                st.rerun()
            if st.button("❓ Help", key="q4", use_container_width=True):
                q = "help"
                st.session_state.chat_history.append({"role": "user", "content": q})
                resp = chatbot.process_query(q)
                st.session_state.chat_history.append({"role": "bot", "content": resp})
                st.rerun()
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    user_input = st.text_input(
        "Type your question",
        key="user_question",
        placeholder="Ask about elections... (e.g., Who won in Nemom?)",
        label_visibility="collapsed"
    )
    
    c1, c2, c3 = st.columns([2, 1, 1])
    with c1:
        if st.button("Send Message", key="send_btn", use_container_width=True, type="primary"):
            if user_input and user_input.strip():
                st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
                resp = chatbot.process_query(user_input.strip())
                st.session_state.chat_history.append({"role": "bot", "content": resp})
                st.rerun()
    with c2:
        if st.button("🗑️ Clear", key="clear_btn", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    with c3:
        if st.button("← Home", key="home_btn", use_container_width=True):
            st.switch_page("app.py")
