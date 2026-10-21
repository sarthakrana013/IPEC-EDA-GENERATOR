import streamlit as st
import pandas as pd
import time

# 1. Page Configuration
st.set_page_config(page_title="EDA Engine Cloud", page_icon="📊", layout="wide", initial_sidebar_state="expanded")

# 2. INJECTING YOUR CUSTOM UI/UX CSS DESIGN
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Import JetBrains Mono from your design */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');

    /* Global Typography & Background matching your Tailwind config */
    html, body, [class*="css"] { 
        font-family: "Times New Roman", Times, Georgia, serif;
        background-color: #f8fafc; 
        color: #0f172a;
    }
    
    /* Force Data & Metrics to use JetBrains Mono */
    code, .stDataFrame, div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Hero Section Styling */
    .hero-title { 
        font-size: 2.8rem; 
        color: #0f172a; 
        font-weight: 700; 
        text-align: center; 
        margin-top: 40px; 
        margin-bottom: 10px; 
    }
    .hero-subtitle { 
        font-size: 1.1rem; 
        color: #475569; 
        text-align: center; 
        margin-bottom: 40px; 
    }

    /* Metric Cards (Matching your top-border Green design) */
    div[data-testid="metric-container"], .custom-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 4px solid #107c41; /* Excel Green */
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    
    .card-title { font-size: 1.1rem; font-weight: bold; color: #0f172a; margin-bottom: 5px; }
    .card-text { font-size: 0.95rem; color: #475569; font-family: 'JetBrains Mono', monospace; font-size: 12px; }

    /* Buttons (Excel Green Theme) */
    .stButton > button {
        background-color: #107c41 !important;
        color: white !important;
        border: none !important;
        border-radius: 6px !important;
        font-family: 'JetBrains Mono', monospace !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover {
        background-color: #0b5c2f !important; /* Darker Green */
    }

    /* Freemium Lock Box */
    .lock-box { 
        border: 1px solid #bbf7d0; 
        background-color: #f0fdf4; 
        padding: 20px; 
        border-radius: 8px; 
        margin-top: 20px; 
    }
    .lock-title { font-weight: bold; color: #107c41; font-size: 1.1rem; margin-bottom: 5px; }
    .lock-text { color: #15803d; font-size: 0.95rem; }
    
    /* Top Header Bar */
    .top-bar {
        background-color: #107c41;
        color: white;
        padding: 10px 20px;
        border-radius: 8px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 12px;
        margin-bottom: 20px;
        text-align: right;
    }
</style>
""", unsafe_allow_html=True)

# 3. Session State for Authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# 4. Clean Sidebar Navigation
with st.sidebar:
    st.markdown("<h3 style='color: #107c41; font-weight: bold;'>EDA Engine Cloud</h3>", unsafe_allow_html=True)
    
    if st.session_state.logged_in:
        st.markdown(f"<p style='color: #475569; font-size: 0.9rem;'>User: {st.session_state.username}</p>", unsafe_allow_html=True)
        if st.button("Sign Out", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
            
    nav = st.radio("Navigate", ["Overview", "Authentication", "Cloud Lite App", "Windows App (Download)"], label_visibility="collapsed")
    st.markdown("<br><hr><p style='color: #94a3b8; font-size: 0.8rem; font-family: monospace;'>v3.2.0 | Streamlit Quota Active</p>", unsafe_allow_html=True)

# ==========================================
# PAGE 1: OVERVIEW (Minimal Landing Page)
# ==========================================
if nav == "Overview":
    st.markdown('<div class="top-bar">STATUS: READY (LOCAL/CLOUD) • LIMIT: 5MB ENFORCED</div>', unsafe_allow_html=True)
    st.markdown('<p class="hero-title">Dataframe Ingestion Pipeline.</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Transform raw, dirty matrices into ML-ready datasets with absolute data privacy.</p>', unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1.5, 1, 1.5])
    with col_btn2:
        if st.button("Launch Application", use_container_width=True, type="primary"):
            st.info("Navigate to 'Authentication' in the sidebar to securely connect.")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="custom-card">
            <div class="card-title">100% Air-Gapped</div>
            <div class="card-text">Desktop execution engine runs natively. Zero data is transmitted to AWS/GCP, ensuring enterprise compliance.</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="custom-card">
            <div class="card-title">Vectorized Cleaning</div>
            <div class="card-text">Autonomously purges regex anomalies, coercing types, and applying statistical median/mode imputation.</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="custom-card">
            <div class="card-title">Deterministic NLP</div>
            <div class="card-text">Query local matrices using standard language. The offline LLM outputs quantitative results instantly.</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# PAGE 2: AUTHENTICATION
# ==========================================
elif nav == "Authentication":
    st.markdown("<h3 style='color: #0f172a; font-weight: bold; text-align: center; margin-bottom: 20px;'>Secure Gateway</h3>", unsafe_allow_html=True)
    
    if st.session_state.logged_in:
        st.success("Session active. You may proceed to the Cloud Lite App or Windows App Download.")
    else:
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            tab1, tab2 = st.tabs(["Sign In", "Register"])
            
            with tab1:
                st.text_input("Email")
                st.text_input("Password", type="password")
                if st.button("Authenticate", use_container_width=True):
                    st.session_state.logged_in = True
                    st.session_state.username = "telemetry-inst-01"
                    st.success("Authenticated.")
                    time.sleep(0.5)
                    st.rerun()
                    
            with tab2:
                st.text_input("Organization")
                st.text_input("Work Email")
                st.text_input("Create Password", type="password")
                if st.button("Provision Account", use_container_width=True):
                    st.session_state.logged_in = True
                    st.session_state.username = "New_Analyst"
                    st.success("Account provisioned.")
                    time.sleep(0.5)
                    st.rerun()

# ==========================================
# PAGE 3: CLOUD LITE APP (The Freemium Funnel)
# ==========================================
elif nav == "Cloud Lite App":
    if not st.session_state.logged_in:
        st.warning("Authentication required to access the cloud sandbox.")
    else:
        st.markdown('<div class="top-bar">SANDBOX ACTIVE: Streamlit Community Cloud (Max 5.0 MB Quota)</div>', unsafe_allow_html=True)
        st.markdown("<h3 style='color: #0f172a; font-weight: bold;'>Dataframe Ingestion Pipeline</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #475569; font-size: 0.95rem; margin-bottom: 20px;'>Upload a sample file to view structural profiling.</p>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("FORMATS: .CSV, .XLSX, .PARQUET, .JSON", type=['csv', 'xlsx', 'json', 'parquet'])
        
        if uploaded_file:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            
            if file_size_mb > 5.0:
                st.error(f"Execution Halted: File exceeds 5.0MB payload limit ({file_size_mb:.2f}MB detected).")
                st.markdown("Navigate to 'Windows App (Download)' for unrestricted local processing.")
            else:
                try:
                    # Universal Reader
                    file_ext = uploaded_file.name.split('.')[-1].lower()
                    if file_ext in ['csv', 'txt']:
                        df = pd.read_csv(uploaded_file)
                    elif file_ext in ['xlsx', 'xls']:
                        df = pd.read_excel(uploaded_file)
                    elif file_ext == 'json':
                        df = pd.read_json(uploaded_file)
                    elif file_ext == 'parquet':
                        df = pd.read_parquet(uploaded_file)
                    
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown("<h4 style='color: #0f172a; font-weight: bold;'>Matrix Dimensionality</h4>", unsafe_allow_html=True)
                    
                    col1, col2, col3 = st.columns(3)
                    col1.metric("TOTAL ROWS", f"{df.shape[0]:,}")
                    col2.metric("COLUMNS", f"{df.shape[1]}")
                    col3.metric("NULL / MISSING", f"{df.isnull().sum().sum():,}")
                    
                    st.markdown("<br><h4 style='color: #0f172a; font-weight: bold;'>Dataframe Slice Inspection (HEAD 5)</h4>", unsafe_allow_html=True)
                    st.dataframe(df.head(), use_container_width=True)
                    
                    st.markdown("""
                    <div class="lock-box">
                        <div class="lock-title">🔒 Pro Engine Analytical Modules Locked</div>
                        <div class="lock-text">Aggressive Auto-Clean Engine, Visual Analytics Suite, and Deterministic NLP Chatbot are disabled in the Cloud Sandbox.<br><br><b>Download the desktop Windows App (.exe) to unlock multi-gigabyte processing, GPU plotting, and offline LLM access.</b></div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Data parse failure. Ensure format is tabular. Error: {e}")

# ==========================================
# PAGE 4: DOWNLOAD APP
# ==========================================
elif nav == "Windows App (Download)":
    st.markdown('<div class="top-bar">ISOLATION: SECURE • VERSION: V3.2.0 STABLE</div>', unsafe_allow_html=True)
    st.markdown("<h3 style='color: #0f172a; font-weight: bold; text-align: center;'>Deploy Local Execution Engine</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569; text-align: center; font-size: 0.95rem; margin-bottom: 40px;'>Acquire the standalone Windows executable for unrestricted usage.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="custom-card" style="margin-bottom: 20px;">
            <div class="card-title">Runtime Capability Matrix</div>
            <ul style="color: #475569; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; line-height: 1.8;">
                <li>OS Requirement: Windows 10/11 (64-bit)</li>
                <li>File Size Quota: UNLIMITED</li>
                <li>Data Privacy: 100% AIR-GAPPED</li>
                <li>Compute Architecture: AVX-512 / CUDA Support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        dummy_exe_bytes = b"Executable build payload placeholder"
        st.download_button(
            label="Download Application (Windows x64)", 
            data=dummy_exe_bytes, 
            file_name="EDA_Engine_V3_Installer.exe", 
            mime="application/octet-stream",
            use_container_width=True,
            type="primary"
        )
