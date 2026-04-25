import streamlit as st
from chatbot import create_chatbot
from faq_data import QUICK_QUESTIONS
import datetime

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Asma — Banking Assistant",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@600;700&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Root & Background ── */
:root {
    --emerald:   #00C896;
    --emerald-d: #00A37A;
    --navy:      #0A1628;
    --navy-2:    #0F2040;
    --navy-3:    #162B52;
    --gold:      #F5C842;
    --text:      #E8EDF5;
    --muted:     #7A8BA8;
    --card:      rgba(15,32,64,0.85);
    --border:    rgba(0,200,150,0.15);
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--navy) !important;
    font-family: 'DM Sans', sans-serif;
    color: var(--text);
}

[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background:
        radial-gradient(ellipse 60% 50% at 80% 10%, rgba(0,200,150,0.08) 0%, transparent 60%),
        radial-gradient(ellipse 40% 40% at 10% 80%, rgba(245,200,66,0.05) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--navy-2) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * { color: var(--text) !important; }

/* ── Header ── */
.Asma-header {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px 0 8px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 24px;
}

.Asma-avatar {
    width: 52px; height: 52px;
    background: linear-gradient(135deg, var(--emerald), var(--emerald-d));
    border-radius: 16px;
    display: flex; align-items: center; justify-content: center;
    font-size: 26px;
    box-shadow: 0 4px 20px rgba(0,200,150,0.35);
    flex-shrink: 0;
}

.Asma-name {
    font-family: 'Playfair Display', serif;
    font-size: 26px;
    font-weight: 700;
    color: var(--text);
    line-height: 1.1;
}

.Asma-sub {
    font-size: 12px;
    color: var(--emerald);
    letter-spacing: 2px;
    text-transform: uppercase;
    font-weight: 500;
}

.online-dot {
    display: inline-block;
    width: 8px; height: 8px;
    background: var(--emerald);
    border-radius: 50%;
    margin-right: 6px;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(1.3); }
}

/* ── Chat messages ── */
[data-testid="stChatMessage"] {
    background: var(--card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 16px !important;
    padding: 16px !important;
    margin-bottom: 12px !important;
    backdrop-filter: blur(10px);
}

[data-testid="stChatMessage"][data-testid*="user"] {
    border-color: rgba(245,200,66,0.2) !important;
    background: rgba(245,200,66,0.05) !important;
}

/* ── Chat input ── */
[data-testid="stChatInput"] {
    background: var(--navy-3) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 14px !important;
    color: var(--text) !important;
}

[data-testid="stChatInput"]:focus-within {
    border-color: var(--emerald) !important;
    box-shadow: 0 0 0 3px rgba(0,200,150,0.15) !important;
}

/* ── Quick question pills ── */
.quick-label {
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 10px;
    font-weight: 500;
}

/* ── Stat cards ── */
.stat-row {
    display: flex;
    gap: 12px;
    margin: 16px 0;
}

.stat-card {
    flex: 1;
    background: var(--navy-3);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px;
    text-align: center;
}

.stat-num {
    font-family: 'Playfair Display', serif;
    font-size: 28px;
    color: var(--emerald);
    font-weight: 700;
    line-height: 1;
}

.stat-lbl {
    font-size: 11px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 4px;
}

/* ── Helpline banner ── */
.helpline {
    background: linear-gradient(135deg, rgba(0,200,150,0.12), rgba(0,200,150,0.05));
    border: 1px solid rgba(0,200,150,0.3);
    border-radius: 12px;
    padding: 14px 18px;
    margin: 20px 0 8px;
    text-align: center;
}

.helpline-num {
    font-family: 'Playfair Display', serif;
    font-size: 20px;
    color: var(--emerald);
    font-weight: 600;
}

.helpline-label {
    font-size: 11px;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

/* ── Buttons ── */
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 13px !important;
    transition: all 0.2s !important;
    width: 100%;
    text-align: left !important;
    padding: 8px 14px !important;
}

.stButton > button:hover {
    border-color: var(--emerald) !important;
    color: var(--emerald) !important;
    background: rgba(0,200,150,0.06) !important;
}

/* Download button */
.stDownloadButton > button {
    background: linear-gradient(135deg, var(--emerald), var(--emerald-d)) !important;
    border: none !important;
    color: var(--navy) !important;
    font-weight: 600 !important;
    border-radius: 10px !important;
    width: 100% !important;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

/* ── Welcome card ── */
.welcome-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 32px;
    text-align: center;
    margin: 20px 0 32px;
    backdrop-filter: blur(10px);
}

.welcome-title {
    font-family: 'Playfair Display', serif;
    font-size: 22px;
    color: var(--text);
    margin-bottom: 10px;
}

.welcome-sub {
    color: var(--muted);
    font-size: 14px;
    line-height: 1.6;
}

.feature-pill {
    display: inline-block;
    background: rgba(0,200,150,0.1);
    border: 1px solid rgba(0,200,150,0.25);
    color: var(--emerald);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 12px;
    margin: 4px;
    font-weight: 500;
}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "chain" not in st.session_state:
    st.session_state.chain = create_chatbot()
    st.session_state.messages = []
    st.session_state.show_welcome = True

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 8px 0 20px;'>
        <div style='font-size:42px; margin-bottom:8px;'>🏦</div>
        <div style='font-family: Playfair Display, serif; font-size:20px; font-weight:700;'>National Bank</div>
        <div style='font-size:11px; color:#00C896; letter-spacing:2px; text-transform:uppercase;'>Pakistan</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Stats
    stats = st.session_state.chain.get_stats()
    st.markdown(f"""
    <div class='stat-row'>
        <div class='stat-card'>
            <div class='stat-num'>{stats['messages']}</div>
            <div class='stat-lbl'>Messages</div>
        </div>
        <div class='stat-card'>
            <div class='stat-num' style='font-size:18px;'>{stats['duration']}</div>
            <div class='stat-lbl'>Session</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Quick questions
    st.markdown("<div class='quick-label'>Quick Questions</div>", unsafe_allow_html=True)
    for q in QUICK_QUESTIONS:
        if st.button(f"→ {q}", key=f"quick_{q}"):
            st.session_state.pending_question = q

    st.markdown("---")

    # Export
    if st.session_state.messages:
        export_text = st.session_state.chain.export_chat()
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        st.download_button(
            label="⬇ Export Chat",
            data=export_text,
            file_name=f"chat_{timestamp}.txt",
            mime="text/plain",
        )

    # Clear
    if st.button("🗑 Clear Conversation"):
        st.session_state.messages = []
        st.session_state.chain.clear_history()
        st.session_state.show_welcome = True
        st.rerun()

    st.markdown("---")

    # Helpline
    st.markdown("""
    <div class='helpline'>
        <div class='helpline-label'>24/7 Emergency Helpline</div>
        <div class='helpline-num'>111-000-111</div>
        <div style='font-size:11px; color:#7A8BA8; margin-top:4px;'>Lost card · Fraud · Urgent</div>
    </div>
    """, unsafe_allow_html=True)

# ── Main area ──────────────────────────────────────────────────────────────────
col_main, col_gap = st.columns([1, 0.001])

with col_main:
    # Header
    st.markdown("""
    <div class='Asma-header'>
        <div class='Asma-avatar'>🤖</div>
        <div>
            <div class='Asma-name'>Asma</div>
            <div class='Asma-sub'>
                <span class='online-dot'></span>Online · Banking Assistant
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Welcome card (shown before first message)
    if st.session_state.show_welcome and not st.session_state.messages:
        st.markdown("""
        <div class='welcome-card'>
            <div style='font-size:48px; margin-bottom:12px;'>👋</div>
            <div class='welcome-title'>Hello! I'm Asma, your banking assistant.</div>
            <div class='welcome-sub'>
                I can help you with account opening, loans, credit cards,<br>
                mobile banking, and all your everyday banking queries.
            </div>
            <div style='margin-top:18px;'>
                <span class='feature-pill'>💳 Cards & Loans</span>
                <span class='feature-pill'>🏦 Accounts</span>
                <span class='feature-pill'>📱 Mobile Banking</span>
                <span class='feature-pill'>🕌 Islamic Banking</span>
                <span class='feature-pill'>🌍 NRP Services</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Render chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"], avatar="🤖" if msg["role"] == "assistant" else "👤"):
            st.markdown(msg["content"])

    # Handle quick question from sidebar
    if "pending_question" in st.session_state:
        q = st.session_state.pop("pending_question")
        st.session_state.show_welcome = False
        st.session_state.messages.append({"role": "user", "content": q})
        with st.chat_message("user", avatar="👤"):
            st.markdown(q)
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Asma is typing..."):
                response = st.session_state.chain.predict(q)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()

    # Chat input
    if prompt := st.chat_input("Ask Asma anything about banking..."):
        st.session_state.show_welcome = False
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Asma is typing..."):
                response = st.session_state.chain.predict(prompt)
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.rerun()