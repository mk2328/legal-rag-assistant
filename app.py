import streamlit as st
import tempfile
import os
from rag.document_manager import DocumentManager
from streamlit_oauth import OAuth2Component
import jwt
os.environ["HF_HUB_DISABLE_SYMLINKS"] = "1"


# ─── Configuration ───
st.set_page_config(
    page_title="Legal AI Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Premium CSS ───
def set_custom_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif !important;
        }

        .stApp {
            background-color: #0a0a0f !important;
        }
                
        /* Google sign in button styling */
        [data-testid="stButton"] > button[kind="googleSignIn"],
        div[class*="stButton"] > button {
            background: white !important;
            color: #1a1a1a !important;
            border: 1px solid #e0e0e0 !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            font-size: 0.95rem !important;
            padding: 10px 24px !important;
            width: 100% !important;
        }

        /* ── Sidebar ── */
        [data-testid="stSidebar"] {
            height: 100vh !important;
            background-color: #0f0f18 !important;
            border-right: 1px solid #252538 !important;
            padding-top: 1rem !important;
        }

        [data-testid="stSidebar"] h1 {
            font-family: 'DM Serif Display', serif !important;
            font-size: 1.3rem !important;
            font-weight: 400 !important;
            color: #ffffff !important;
            letter-spacing: 0.01em !important;
            margin-top: -40px !important;
            margin-bottom: 4px !important;
        }

        [data-testid="stSidebar"] h3 {
            font-size: 0.68rem !important;
            font-weight: 700 !important;
            color: #5555aa !important;
            text-transform: uppercase !important;
            letter-spacing: 0.14em !important;
            margin-bottom: 10px !important;
            margin-top: 4px !important;
        }

        [data-testid="stSidebar"] hr {
            border-color: #252538 !important;
            margin: 8px 0 !important;
        }

        [data-testid="stSidebar"] .stButton {
            margin-bottom: 2px !important;
        }

        [data-testid="stFileUploader"] {
            background-color: #14141f !important;
            border: 1px dashed #303055 !important;
            border-radius: 10px !important;
            padding: 4px !important;
        }

        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 1rem !important;
            max-width: 1200px !important;
        }

        h1 { margin-top: -10px !important; }

        /* ── Hero ── */
        .hero-section {
            background: linear-gradient(135deg, #0f0f1e 0%, #1a1035 50%, #0f0f1e 100%);
            border: 1px solid #2e2860;
            border-radius: 20px;
            padding: 48px 48px 40px;
            margin-bottom: 32px;
            position: relative;
            overflow: hidden;
        }

        .hero-section::before {
            content: '';
            position: absolute;
            top: -80px; right: -80px;
            width: 300px; height: 300px;
            background: radial-gradient(circle, rgba(108,99,255,0.22) 0%, transparent 65%);
            pointer-events: none;
        }

        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(108,99,255,0.18);
            border: 1px solid rgba(108,99,255,0.45);
            border-radius: 20px;
            padding: 5px 14px;
            font-size: 0.7rem;
            color: #c4beff;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            margin-bottom: 20px;
        }

        .hero-title {
            font-family: 'DM Serif Display', serif !important;
            font-size: 2.8rem;
            font-weight: 400;
            color: #f5f3ff;
            line-height: 1.15;
            margin: 0 0 14px 0;
        }

        .hero-subtitle {
            font-size: 1rem;
            color: #9090bb;
            font-weight: 400;
            margin: 0 0 32px 0;
            line-height: 1.7;
            max-width: 500px;
        }

        .hero-stats { display: flex; gap: 36px; }

        .hero-stat-number {
            font-size: 1.6rem;
            font-weight: 700;
            color: #a89dff;
            display: block;
            line-height: 1;
            margin-bottom: 4px;
        }

        .hero-stat-label {
            font-size: 0.68rem;
            color: #666688;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }

        /* ── Section label ── */
        .section-label {
            font-size: 0.68rem;
            font-weight: 700;
            color: #666688;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            margin-bottom: 14px;
        }

        /* ── Document cards ── */
        .doc-card {
            background: #0f0f18;
            border: 1px solid #252538;
            border-radius: 14px;
            padding: 22px 22px 16px;
            transition: all 0.25s ease;
            margin-bottom: 2px;
            position: relative;
            overflow: hidden;
        }

        .doc-card:hover {
            border-color: #7c6fff;
            background: #13122a;
            transform: translateY(-4px);
            box-shadow: 0 16px 32px rgba(108,99,255,0.2);
        }

        .doc-card::after {
            content: '';
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, #6c63ff, #a78bfa);
            opacity: 0;
            transition: opacity 0.25s;
        }

        .doc-card:hover::after { opacity: 1; }

        .doc-card-icon {
            font-size: 1.8rem;
            margin-bottom: 14px;
            display: block;
        }

        .doc-card-name {
            font-size: 1rem;
            font-weight: 600;
            color: #e8e4ff;
            margin-bottom: 8px;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
        }

        .doc-card-meta {
            font-size: 0.72rem;
            color: #555577;
            text-transform: uppercase;
            letter-spacing: 0.08em;
        }

        /* ── Empty state ── */
        .empty-state {
            text-align: center;
            padding: 70px 20px;
            border: 1px dashed #252538;
            border-radius: 16px;
            background: #0a0a12;
        }

        .empty-icon { font-size: 3.2rem; margin-bottom: 18px; opacity: 0.5; }
        .empty-title { font-size: 1.1rem; font-weight: 600; color: #666688; margin-bottom: 8px; }
        .empty-text { font-size: 0.85rem; color: #444466; }

        /* ── Chat header ── */
        .chat-header {
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 16px 20px;
            background: #0f0f18;
            border: 1px solid #252538;
            border-radius: 14px;
            margin-bottom: 16px;
        }

        .chat-icon-box {
            width: 40px; height: 40px;
            background: rgba(108,99,255,0.15);
            border: 1px solid rgba(108,99,255,0.3);
            border-radius: 10px;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.2rem; flex-shrink: 0;
        }

        .chat-doc-name {
            font-size: 1.05rem;
            font-weight: 600;
            color: #e8e4ff;
            margin-bottom: 3px;
        }

        .chat-doc-status {
            font-size: 0.72rem;
            color: #44cc88;
            font-weight: 500;
        }

        /* ── Chat messages ── */
        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
            background: #141428 !important;
            border: 1px solid #252548 !important;
            border-radius: 12px !important;
            padding: 12px 18px !important;
            margin: 6px 0 !important;
        }

        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
            background: #0f0f1e !important;
            border: 1px solid #1e1e38 !important;
            border-radius: 12px !important;
            padding: 12px 18px !important;
            margin: 6px 0 !important;
        }

        /* ── Chat Input - Clean Background + No Overlapping on Scroll (Final Fix 2026) ── */

        [data-testid="stChatInput"] {
            background: transparent !important;
            z-index: 100 !important;
        }

        [data-testid="stChatInput"] > div {
            background: #0f0f18 !important;           /* ← Yeh tumhara desired dark background */
            border: 1px solid #303055 !important;
            border-radius: 12px !important;
            box-shadow: none !important;
        }

        /* Inner layers jo grey box bana rahe the */
        [data-testid="stChatInput"] > div > div,
        [data-testid="stChatInput"] > div > div > div,
        .stChatInput div[data-baseweb="textarea"] {
            background: transparent !important;
        }

        /* Textarea */
        [data-testid="stChatInput"] textarea {
            background: transparent !important;
            color: #e8e4ff !important;
            caret-color: #7c6fff !important;
        }

        /* Placeholder */
        [data-testid="stChatInput"] textarea::placeholder {
            color: #777799 !important;
        }

        /* Focus glow */
        [data-testid="stChatInput"] > div:focus-within {
            border-color: #7c6fff !important;
            box-shadow: 0 0 0 3px rgba(108,99,255,0.18) !important;
        }

        /* Yeh sabse important hai → scrolling ke time background fix */
        [data-testid="stBottom"] > div,
        [data-testid="stChatFloatingInputContainer"] {
            background: #0f0f18 !important;     /* App ka main dark background */
            padding-bottom: 16px !important;
        }

        /* Extra safety for any remaining emotion cache layers */
        .st-emotion-cache-1c7y2kd,
        div[data-testid="stChatInput"] * {
            background-color: transparent !important;
        }

        /* ── Reduce extra space below chat input ── */
        [data-testid="stBottom"] > div,
        [data-testid="stChatFloatingInputContainer"] {
            background: #0f0f18 !important;     /* ya jo bhi tumhara desired dark color hai */
            padding-bottom: 0px !important;     /* yeh main fix hai – 16px se kam kiya */
            padding-top: 4px !important;
            margin-bottom: 0 !important;
        }

        /* Input box ko thoda upar shift karne ke liye (optional but clean look) */
        [data-testid="stChatInput"] {
            margin-bottom: 0 !important;
        }

        /* Agar phir bhi thoda space lage toh yeh bhi add kar do */
        .st-emotion-cache-1c7y2kd,
        div[data-testid="stBottom"] {
            padding-bottom: 0px !important;
        }
            

        /* ── Buttons ── */
        .stButton > button[kind="primary"] {
            background-color: #2e2860 !important; /* Darker solid color */
            border: 1px solid #453c99 !important;
            border-radius: 8px !important;
            font-weight: 900 !important;
            color: #ffffff !important;
            letter-spacing: 0.02em !important;
            transition: all 0.2s !important;
        }

        .stButton > button[kind="primary"]:hover {
            transform: translateY(-1px) !important;
            box-shadow: 0 8px 20px rgba(108,99,255,0.45) !important;
            background-color: #3d3780 !important;
            border-color: #6c63ff !important;
        }

        .stButton > button[kind="secondary"] {
            background: #14141f !important;
            border: 1px solid #303055 !important;
            color: #9090bb !important;
            border-radius: 8px !important;
        }

        .stButton > button[kind="secondary"]:hover {
            border-color: #7c6fff !important;
            color: #c4beff !important;
        }

        /* ── Sidebar footer ── */
        .sidebar-footer-box {
            background: #0a0a14;
            border: 1px solid #1e1e38;
            border-radius: 10px;
            padding: 12px 14px;
            margin-top: 8px;
        }

        /* ── Global text brightness fix ── */
        p, li { color: #ccccee !important; }
        .stMarkdown p { color: #ccccee !important; }

        /* ── Login page full-screen centering ── */
        .login-wrapper {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 80vh;
            width: 100%;
        }

        .login-card {
            background: linear-gradient(145deg, #0f0f1e 0%, #16123a 50%, #0f0f1e 100%);
            border: 1px solid #2e2860;
            border-radius: 24px;
            padding: 48px 44px 40px;
            padding-top:20px!important;
            padding-bottom:20px!important;
            width: 100%;
            max-width: 500px;
            text-align: center;
            position: relative;
            overflow: hidden;
            box-shadow: 0 24px 64px rgba(0,0,0,0.6), 0 0 0 1px rgba(108,99,255,0.08);
            margin-bottom:3%;
            margin-top:7%
        }

        .login-card::before {
            content: '';
            position: absolute;
            top: -100px; right: -100px;
            width: 280px; height: 280px;
            background: radial-gradient(circle, rgba(108,99,255,0.2) 0%, transparent 65%);
            pointer-events: none;
        }

        .login-card::after {
            content: '';
            position: absolute;
            bottom: -80px; left: -80px;
            width: 220px; height: 220px;
            background: radial-gradient(circle, rgba(167,139,250,0.12) 0%, transparent 65%);
            pointer-events: none;
        }

        
        /* ── Loading screen ── */
        .loading-screen {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            min-height: 60vh;
            gap: 20px;
        }

        .loading-spinner {
            width: 48px;
            height: 48px;
            border: 3px solid #252548;
            border-top: 3px solid #7c6fff;
            border-radius: 50%;
            animation: spin 0.9s linear infinite;
        }

        @keyframes spin {
            to { transform: rotate(360deg); }
        }

        .loading-text {
            font-size: 1rem;
            color: #9090bb;
            font-weight: 500;
            letter-spacing: 0.02em;
        }

        .loading-sub {
            font-size: 0.78rem;
            color: #555577;
        }

        /* ── Chat message improved formatting ── */
        [data-testid="stChatMessage"] {
            border-radius: 14px !important;
            padding: 14px 18px !important;
            margin: 8px 0 !important;
        }

        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
            background: linear-gradient(135deg, #141428 0%, #1a1840 100%) !important;
            border: 1px solid #2d2b55 !important;
        }

        [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
            background: linear-gradient(135deg, #0f0f1e 0%, #13112a 100%) !important;
            border: 1px solid #1e1e38 !important;
        }

        [data-testid="stChatMessage"] p {
            color: #ddd8ff !important;
            font-size: 0.92rem !important;
            line-height: 1.7 !important;
        }
                
        /* ── Logout Confirmation Modal (Center + Nice Look) ── */
                        /* ── Logout Confirmation Modal (Full Center Popup) ── */
        .logout-modal {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            width: 100vw !important;
            height: 100vh !important;
            background: rgba(10, 10, 15, 0.92) !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            z-index: 10000 !important;
        }

        .logout-modal-content {
            background: #1a1a28 !important;
            border: 1px solid #4a2f2f !important;
            border-radius: 20px !important;
            padding: 40px 36px 32px !important;
            width: 380px !important;
            text-align: center !important;
            box-shadow: 0 25px 70px rgba(0, 0, 0, 0.8) !important;
        }

        .logout-modal-content h3 {
            color: #ff8a8a !important;
            margin-bottom: 12px !important;
            font-size: 1.35rem !important;
        }

        /* Red Yes Button */
        .stButton > button[key="confirm_yes"] {
            background-color: #3a1f1f !important;
            border: 1px solid #e06666 !important;
            color: #ffaaaa !important;
            font-weight: 600 !important;
            width: 100% !important;
        }

        .stButton > button[key="confirm_yes"]:hover {
            background-color: #4f2a2a !important;
            border-color: #ff7777 !important;
            color: #ffc1c1 !important;
        }

        /* Cancel Button */
        .stButton > button[key="confirm_no"] {
            background-color: #242438 !important;
            border: 1px solid #555577 !important;
            color: #b0b0dd !important;
            width: 100% !important;
        }
        

    </style>
    """, unsafe_allow_html=True)

set_custom_css()



# ─── Helper functions to get credentials from .env or secrets ───
def get_secret(key: str, default: str = "") -> str:
    # try streamlit secrets first (Streamlit Cloud)
    try:
        val = st.secrets.get(key)
        if val:
            return val
    except:
        pass
    # fall back to .env (local development)
    return os.getenv(key, default)

client_id = get_secret("GOOGLE_CLIENT_ID")
client_secret = get_secret("GOOGLE_CLIENT_SECRET")

# ─── Google Auth Setup ───
oauth2 = OAuth2Component(
    client_id=client_id, 
    client_secret=client_secret, 
    authorize_endpoint="https://accounts.google.com/o/oauth2/auth",
    token_endpoint="https://oauth2.googleapis.com/token"
)

# ─── Authentication Flow ───

# Step 1: No token → show login page and stop
if "token" not in st.session_state:
    # Hide sidebar on login page
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { display: none !important; }
            .block-container { padding-top: 0 !important; max-width: 100% !important; }
        </style>
    """, unsafe_allow_html=True)

    # Center the login card using columns
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("""
        <div class="login-card">
            <div style='font-size:3.2rem; margin-bottom:18px; filter: drop-shadow(0 0 20px rgba(108,99,255,0.4))'>⚖️</div>
            <div style='font-family: DM Serif Display, serif; font-size:2.1rem;
                        color:#f5f3ff; font-weight:400; margin-bottom:10px; line-height:1.2'>
                Legal RAG Assistant
            </div>
            <div style='color:#9090bb; font-size:0.92rem; margin-bottom:30px; line-height:1.7'>
                Your intelligent partner for<br>legal document analysis.
            </div>
            <div style='width:48px; height:1px; background:linear-gradient(90deg, transparent, #7c6fff, transparent); margin: 0 auto 28px;'></div>
        </div>
        
        <div style="display: flex; justify-content: center; width: 100%;">
        """, unsafe_allow_html=True)


        # get redirect uri automatically based on environment
        redirect_uri = get_secret("GOOGLE_REDIRECT_URI", "http://localhost:8501")

        result = oauth2.authorize_button(
            name="Sign in with Google",
            redirect_uri=redirect_uri,
            scope="openid email profile",
            icon="google",
        )

        st.markdown("""
        <p style='text-align:center; color:#444466; font-size:0.75rem; margin-top:16px'>
            🔒 Your documents are private and secure.<br>
            We only use your Google account to identify you.
        </p>
        """, unsafe_allow_html=True)

    if result:
        st.session_state.token = result.get("token")
        st.session_state.just_logged_in = True
        st.rerun()

    st.stop()  # Stop here — nothing below runs without a token

# Step 2: Token exists but user just logged in → show loading screen
import time
# After successful login (token set hone ke baad)
if st.session_state.get("just_logged_in", False):
    st.session_state.just_logged_in = False
    
    # Hide sidebar during loading
    st.markdown("""
        <style>
            [data-testid="stSidebar"] { display: none !important; }
            .block-container { padding-top: 0 !important; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("""
        <div class='loading-screen'>
            <div class='loading-spinner'></div>
            <div>
                <div class='loading-text'>Setting up your workspace...</div>
                <div class='loading-sub' style='margin-top:8px;'>
                    Loading documents & preparing AI assistant
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Thoda longer delay + force rerun
    time.sleep(1.8)        # 1.2 se badha diya taaki dikhe
    st.rerun()

    
# Step 3: Token exists and ready → decode and continue
token = st.session_state.token
id_token = token.get("id_token")
token_data = jwt.decode(id_token, options={"verify_signature": False})

user_email = token_data.get("email", "user@example.com")
user_name = token_data.get("name", "User")

# ─── Logout Helper ───
def logout():
    del st.session_state.token
    st.rerun()

# ─── Your Application Logic Starts Here ───
@st.cache_resource
def get_manager(email: str):
    safe_email = email.replace("@", "_").replace(".", "_")
    return DocumentManager(base_dir=f"documents/{safe_email}")

manager = get_manager(user_email)


# ─── Sidebar ────────────────────────────────────────
with st.sidebar:
    st.title("⚖️ Legal Assistant")
    st.write("---")

    # user info + logout
        # User Info
    st.markdown(
        f"<div style='display:flex;align-items:center;gap:8px;margin-bottom:8px'>"
        f"<div style='width:28px;height:28px;background:rgba(108,99,255,0.2);"
        f"border:1px solid rgba(108,99,255,0.3);border-radius:50%;"
        f"display:flex;align-items:center;justify-content:center;font-size:0.8rem'>👤</div>"
        f"<div style='font-size:0.78rem;color:#9090bb'>{user_name}</div>"
        f"</div>",
        unsafe_allow_html=True
    )

    # Logout Button
        # Logout Button
    if st.button("Logout", type="secondary", use_container_width=True):
        st.session_state.confirm_logout = True

    # Dialog based confirmation (Better approach)
    @st.dialog("Confirm Logout")
    def show_logout_dialog():
        st.markdown("### 👋 Confirm Logout?")
        st.write("You will be signed out from your account.\nAll unsaved changes will be kept.")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("✓ Yes, Logout", type="primary"):
                logout()
                st.rerun()
        with col2:
            if st.button("✗ Cancel"):
                st.rerun()

    if st.session_state.get("confirm_logout"):
        show_logout_dialog()
        st.session_state.confirm_logout = False   # reset after showing

    st.write("---")

    st.subheader("Upload Document")
    uploaded_file = st.file_uploader("", type="pdf", label_visibility="collapsed")

    if uploaded_file:
        doc_name = uploaded_file.name.replace(".pdf", "")
        if st.button("Process Document", type="primary", use_container_width=True):
            with st.spinner("Analyzing document..."):
                with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name
                manager.index_document(tmp_path, doc_name)
                os.unlink(tmp_path)
            st.rerun()

    st.write("---")

    st.subheader("📂 Saved Documents")
    saved_docs = manager.get_saved_documents()

    if saved_docs:
        for doc in saved_docs:
            col1, col2 = st.columns([4, 1])
            with col1:
                is_active = st.session_state.get("active_doc") == doc
                if st.button(
                    f"📄 {doc}",
                    key=f"side_{doc}",
                    use_container_width=True,
                    type="primary" if is_active else "secondary"
                ):
                    st.session_state.active_doc = doc
                    st.rerun()
            with col2:
                if st.button("🗑️", key=f"del_{doc}"):
                    manager.delete_document(doc)
                    if st.session_state.get("active_doc") == doc:
                        del st.session_state.active_doc
                    st.rerun()
    else:
        st.markdown(
            "<p style='color:#444466;font-size:0.8rem;text-align:center;padding:10px 0'>"
            "No documents yet</p>",
            unsafe_allow_html=True
        )

    st.write("---")
    st.markdown(
        "<div class='sidebar-footer-box'>"
        "<p style='color:#7c6fff !important;font-size:0.68rem;font-weight:700;"
        "letter-spacing:0.1em;text-transform:uppercase;margin:0 0 8px'>Tech Stack</p>"
        "<p style='color:#7777aa !important;font-size:0.75rem;margin:0;line-height:1.8'>"
        "Streamlit · Python · RAG Pipeline<br>FAISS · Groq API · LangChain</p>"
        "</div>"
        "<p style='color:#444466 !important;font-size:0.72rem;text-align:center;"
        "margin-top:12px;margin-bottom:0'>"
        "Built by <span style='color:#7c6fff;font-weight:600'>Muskan Kamran</span></p>",
        unsafe_allow_html=True
    )

# ─── Main Area ──────────────────────────────────────
active_doc = st.session_state.get("active_doc")

if not active_doc:

    doc_count = len(saved_docs) if saved_docs else 0
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-badge">⚖️ &nbsp; AI-Powered Legal Analysis</div>
        <div class="hero-title">Your Legal Documents,<br>Instantly Understood.</div>
        <div class="hero-subtitle">
            Upload any legal contract, NDA, or agreement — ask questions
            in plain English and get precise, context-aware answers instantly.
        </div>
        <div class="hero-stats">
            <div class="hero-stat">
                <span class="hero-stat-number">{doc_count}</span>
                <span class="hero-stat-label">Documents</span>
            </div>
            <div class="hero-stat">
                <span class="hero-stat-number">RAG</span>
                <span class="hero-stat-label">Powered</span>
            </div>
            <div class="hero-stat">
                <span class="hero-stat-number">Groq</span>
                <span class="hero-stat-label">LLM</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if saved_docs:
        st.markdown("<div class='section-label'>Your Documents</div>", unsafe_allow_html=True)
        cols = st.columns(3)
        for i, doc in enumerate(saved_docs):
            with cols[i % 3]:
                st.markdown(f"""
                <div class="doc-card">
                    <span class="doc-card-icon">📄</span>
                    <div class="doc-card-name">{doc}</div>
                    <div class="doc-card-meta">PDF · Legal Document</div>
                </div>
                """, unsafe_allow_html=True)
                if st.button("Open →", key=f"card_{doc}", use_container_width=True, type="primary"):
                    st.session_state.active_doc = doc
                    st.rerun()
    else:
        st.markdown("""
        <div class="empty-state">
            <div class="empty-icon">📂</div>
            <div class="empty-title">No documents yet</div>
            <div class="empty-text">Upload a PDF from the sidebar to get started.</div>
        </div>
        """, unsafe_allow_html=True)

else:
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown(f"""
        <div class="chat-header">
            <div class="chat-icon-box">📄</div>
            <div>
                <div class="chat-doc-name">{active_doc}</div>
                <div class="chat-doc-status">● Active · Ready to answer</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)
        if st.button("Clear Chat", type="secondary", use_container_width=True):
            manager.clear_chat(active_doc)
            st.rerun()

    chat_container = st.container(height=560)
    pipeline = manager.load_document(active_doc)
    chat_history = manager.get_chat_history(active_doc)

    with chat_container:
        if not chat_history:
            st.markdown("""
            <div style='text-align:center; padding:60px 20px;'>
                <div style='
                    width:64px; height:64px;
                    background:rgba(108,99,255,0.12);
                    border:1px solid rgba(108,99,255,0.25);
                    border-radius:16px;
                    display:flex; align-items:center; justify-content:center;
                    font-size:1.8rem;
                    margin: 0 auto 20px;
                '>💬</div>
                <div style='font-size:1rem; font-weight:600; color:#8888bb; margin-bottom:8px;'>
                    Ask anything about this document
                </div>
                <div style='font-size:0.8rem; color:#555577; line-height:1.7;'>
                    Try: <span style='color:#7c6fff'>"Summarize this document"</span> or <span style='color:#7c6fff'>"What are the key clauses?"</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

        for msg in chat_history:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

    if question := st.chat_input(f"Ask about {active_doc}..."):
        with chat_container:
            with st.chat_message("user"):
                st.write(question)
        manager.add_message(active_doc, "user", question)

    

        with chat_container:
            with st.chat_message("assistant"):
                with st.spinner("Analyzing..."):
                    answer = pipeline.ask(question)
                st.write(answer)
        manager.add_message(active_doc, "assistant", answer)
        st.rerun()