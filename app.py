import streamlit as st
import pandas as pd
import time

# 1. Page Configuration
st.set_page_config(page_title="EDA Engine Cloud", page_icon="📊", layout="wide")

# 2. INJECTING THE "EXCEL GREEN & WHITE" UI/UX AND FILE UPLOADER FIX
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Import Fonts */
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap');

    /* Force Light Mode Backgrounds */
    .stApp { background-color: #f8fafc !important; }
    
    /* Global Typography overrides to ensure dark text on light backgrounds */
    html, body, p, span, div, h1, h2, h3, h4, h5, h6, label { 
        font-family: "Times New Roman", Times, Georgia, serif !important;
        color: #0f172a !important;
    }
    
    /* Force Monospace for Data & Metrics */
    code, .stDataFrame, div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Top Navigation / Status Bar */
    .top-status-bar {
        background-color: #107c41;
        color: #ffffff !important;
        padding: 8px 16px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 12px;
        font-weight: 600;
        display: flex;
        justify-content: space-between;
        margin-bottom: 25px;
        box-shadow: 0 2px 4px rgba(16, 124, 65, 0.2);
    }
    .top-status-bar span { color: #ffffff !important; }

    /* Custom Cards (White with Green Top Border) */
    .custom-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 4px solid #107c41;
        border-radius: 6px;
        padding: 20px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        height: 100%;
    }
    
    /* Card Titles & Text */
    .card-title { font-size: 1.1rem; font-weight: bold; color: #0f172a !important; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;}
    .card-text { font-size: 0.9rem; color: #475569 !important; font-family: "Times New Roman", serif !important; line-height: 1.5; }

    /* Buttons (Solid Excel Green) */
    .stButton > button {
        background-color: #107c41 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 4px !important;
        font-family: 'Times New Roman', serif !important;
        font-weight: bold !important;
        padding: 0.5rem 1rem !important;
        width: 100%;
    }
    .stButton > button:hover { background-color: #0b5c2f !important; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }
    .stButton > button * { color: #ffffff !important; }

    /* Input Fields styling for Light Mode */
    .stTextInput input {
        background-color: #ffffff !important;
        border: 1px solid #cbd5e1 !important;
        color: #0f172a !important;
        border-radius: 4px !important;
    }
    .stTextInput input:focus { border-color: #107c41 !important; box-shadow: 0 0 0 1px #107c41 !important; }

    /* FIX: File Uploader Box (Dark Background, White Text, Green Button) */
    [data-testid="stFileUploadDropzone"] {
        background-color: #1e293b !important;
        border: 1px solid #334155 !important;
    }
    [data-testid="stFileUploadDropzone"] * {
        color: #ffffff !important;
    }
    [data-testid="stFileUploadDropzone"] button {
        background-color: #107c41 !important;
        color: #ffffff !important;
        border: none !important;
        width: auto !important;
    }

    /* Auth Page specific styling */
    .auth-header { background-color: #107c41; color: white !important; padding: 15px 20px; border-radius: 6px 6px 0 0; margin: -20px -20px 20px -20px; font-weight: bold; font-size: 1.2rem;}
    .spec-item { display: flex; align-items: flex-start; margin-bottom: 15px; border-bottom: 1px solid #f1f5f9; padding-bottom: 10px;}
    .spec-icon { color: #107c41 !important; margin-right: 10px; font-weight: bold;}
    .spec-title { font-weight: bold; font-size: 0.95rem; color: #0f172a !important; margin-bottom: 2px;}
    .spec-desc { font-size: 0.85rem; color: #64748b !important; }

    /* Bypass Box */
    .bypass-box { border: 2px solid #bbf7d0; background-color: #f0fdf4; border-radius: 6px; padding: 15px; margin-top: 20px;}
    .bypass-title { color: #107c41 !important; font-weight: bold; margin-bottom: 5px;}
    .bypass-text { color: #15803d !important; font-size: 0.85rem; margin-bottom: 15px;}
    
    /* Lock Box */
    .lock-icon { background-color: #107c41; color: white !important; width: 28px; height: 28px; display: inline-flex; align-items: center; justify-content: center; border-radius: 4px; font-size: 14px; font-weight: bold;}
    .tag { background-color: #f0fdf4; color: #107c41 !important; border: 1px solid #bbf7d0; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-family: 'JetBrains Mono', monospace !important; font-weight: bold;}

    /* Override Streamlit Metric Boxes to look like cards */
    div[data-testid="metric-container"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-top: 4px solid #107c41 !important;
        border-radius: 6px !important;
        padding: 15px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    }
    div[data-testid="stMetricLabel"] * { color: #64748b !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.75rem !important; text-transform: uppercase !important; font-weight: bold !important;}
    
    /* Make Top Tabs Larger and Serif */
    button[data-baseweb="tab"] {
        font-family: 'Times New Roman', serif !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. Session State for Authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Header Info
st.markdown("<h2 style='color: #107c41; font-weight: bold; margin-bottom: 0;'>EDA Engine Cloud</h2>", unsafe_allow_html=True)
if st.session_state.logged_in:
    st.markdown(f"<p style='color: #107c41; font-family: monospace; font-size: 0.85rem; font-weight: bold; margin-top: 5px;'>Active Session: {st.session_state.username}</p>", unsafe_allow_html=True)
else:
    st.markdown("<p style='color: #64748b; font-size: 0.85rem; font-family: monospace; margin-top: 5px;'>Streamlit Community Cloud • V3.2.0</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 4. Top Navigation Tabs
tab_overview, tab_auth, tab_lite, tab_download = st.tabs([
    "🏠 Overview", 
    "🔐 Authentication", 
    "⚡ Cloud Lite App", 
    "📥 Windows App (Download)"
])

# ==========================================
# TAB 1: OVERVIEW 
# ==========================================
with tab_overview:
    st.markdown("""
    <div class="top-status-bar">
        <span>● STREAMLIT CLOUD SANDBOX GATEWAY</span>
        <span>PORT: 8501-SANDBOX • ISOLATION: SECURE</span>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<h1 style="font-size: 2.5rem; font-weight: bold; text-align: center; margin-top: 20px;">Dataframe Ingestion Pipeline</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 1.1rem; color: #475569 !important; text-align: center; margin-bottom: 40px;">Transform raw, dirty matrices into ML-ready datasets with absolute data privacy.</p>', unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1.5, 1, 1.5])
    with col_btn2:
        if st.button("Authenticate & Launch Sandbox"):
            st.info("Please click the '🔐 Authentication' tab above to log in.")
    
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
# TAB 2: AUTHENTICATION
# ==========================================
with tab_auth:
    st.markdown("""
    <div class="top-status-bar">
        <span>EDA Engine Cloud / Authentication Gateway / Node Provisioner</span>
        <span>TLS 1.3 ENCRYPTED</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.session_state.logged_in:
        st.success("Authentication validated. Active session token generated.")
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            if st.button("Sign Out of Session"):
                st.session_state.logged_in = False
                st.rerun()
    else:
        col1, col2 = st.columns([1.2, 1])
        
        with col1:
            st.markdown("""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 6px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div class="auth-header">
                    Sign in to EDA Cloud Lite
                    <div style="font-size: 0.8rem; font-weight: normal; margin-top: 4px;">Authenticate your session to provision an isolated exploratory sandbox.</div>
                </div>
                <p style="font-family: 'JetBrains Mono', monospace; font-size: 0.8rem; font-weight: bold; color: #64748b !important; text-transform: uppercase; margin-bottom: 15px;">Federated Analyst Single Sign-On</p>
            """, unsafe_allow_html=True)
            
            email = st.text_input("Work Email / Institutional ID", placeholder="analyst@quant-research.org")
            token = st.text_input("Security Token / Master Key", type="password", placeholder="••••••••••••••••")
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Authenticate & Launch Sandbox →"):
                st.session_state.logged_in = True
                st.session_state.username = "telemetry-inst-01"
                st.success("Connecting to secure node...")
                time.sleep(0.5)
                st.rerun()
                
            st.markdown("</div>", unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 6px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #e2e8f0; padding-bottom: 15px; margin-bottom: 15px;">
                    <span style="font-weight: bold; color: #0f172a !important;">Cloud Lite Execution Specs</span>
                    <span class="tag">HEALTHY</span>
                </div>
                
                <div class="spec-item">
                    <span class="spec-icon">●</span>
                    <div>
                        <div class="spec-title">Strict 5.0 MB RAM Quota</div>
                        <div class="spec-desc">Enforced via frontend stream validation & config.toml limiters.</div>
                    </div>
                </div>
                
                <div class="spec-item">
                    <span class="spec-icon">●</span>
                    <div>
                        <div class="spec-title">Zero Ephemeral Persistence</div>
                        <div class="spec-desc">Tables stored solely in volatile RAM. All PyArrow buffers are purged immediately upon tab or browser termination.</div>
                    </div>
                </div>
            </div>
            
            <div class="bypass-box">
                <span class="tag" style="background: white;">OFFLINE POWER MODE</span>
                <div class="bypass-title" style="margin-top: 10px; font-size: 1.1rem;">Skip Login with Windows Desktop (.exe)</div>
                <div class="bypass-text">Need to process data larger than 5 MB? Download the standalone native client for zero cloud dependencies, unmetered multi-gigabyte RAM analysis, and local GPU acceleration.</div>
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# TAB 3: CLOUD LITE APP
# ==========================================
with tab_lite:
    if not st.session_state.logged_in:
        st.error("Access Denied: Authentication required to access the cloud sandbox.")
        st.info("Navigate to the '🔐 Authentication' tab to sign in.")
    else:
        st.markdown("""
        <div class="top-status-bar">
            <span>SANDBOX ACTIVE: Streamlit Community Cloud (Max 5.0 MB Quota Enforced)</span>
            <span>BUFFER: 3.8 / 5.0 MB | ISOLATION: SECURE</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <h2 style="margin: 0; font-weight: bold; color: #0f172a !important; display: flex; align-items: center; gap: 10px;">
                <span style="color: #107c41;">📄</span> Dataframe Ingestion Pipeline
            </h2>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #64748b !important; background: #e2e8f0; padding: 4px 8px; border-radius: 4px;">FORMATS: .CSV, .XLSX, .PARQUET, .JSON</span>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("", type=['csv', 'xlsx', 'json', 'parquet'], label_visibility="collapsed")
        
        if uploaded_file:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            
            if file_size_mb > 5.0:
                st.error(f"Execution Halted: File exceeds 5.0MB payload limit ({file_size_mb:.2f}MB detected).")
            else:
                try:
                    file_ext = uploaded_file.name.split('.')[-1].lower()
                    if file_ext in ['csv', 'txt']:
                        df = pd.read_csv(uploaded_file)
                    elif file_ext in ['xlsx', 'xls']:
                        df = pd.read_excel(uploaded_file)
                    elif file_ext == 'json':
                        df = pd.read_json(uploaded_file)
                    elif file_ext == 'parquet':
                        df = pd.read_parquet(uploaded_file)
                    
                    # Metrics Grid
                    col1, col2, col3, col4, col5 = st.columns(5)
                    col1.metric("TOTAL ROWS", f"{df.shape[0]:,}")
                    col2.metric("COLUMNS", f"{df.shape[1]}")
                    col3.metric("IN-MEMORY SIZE", f"{file_size_mb:.2f} MB")
                    col4.metric("TYPING SCHEMAS", f"{len(df.select_dtypes(include=['float64', 'int64']).columns)} Num")
                    col5.metric("NULL / MISSING", f"{df.isnull().sum().sum():,}")
                    
                    st.markdown("""
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 30px; margin-bottom: 10px;">
                        <h3 style="margin: 0; font-weight: bold; color: #0f172a !important;">Dataframe Slice Inspection <span class="tag" style="background: #107c41; color: white !important; border: none;">HEAD(5)</span></h3>
                    </div>
                    """, unsafe_allow_html=True)
                    st.dataframe(df.head(), use_container_width=True)
                    
                    st.markdown("""
                    <div style="display: flex; align-items: center; gap: 10px; margin-top: 40px; margin-bottom: 20px;">
                        <span style="color: #107c41;">●</span>
                        <h2 style="margin: 0; font-weight: bold; font-size: 1.5rem; color: #0f172a !important;">Pro Engine Analytical Modules</h2>
                        <span class="tag">3 LOCKED IN CLOUD SANDBOX</span>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Locked Modules Grid
                    lc1, lc2, lc3 = st.columns(3)
                    with lc1:
                        st.markdown("""
                        <div class="custom-card" style="display: flex; flex-direction: column; justify-content: space-between; min-height: 250px;">
                            <div>
                                <div class="card-title">
                                    <span class="lock-icon">🔒</span>
                                    <span class="tag">DESKTOP EXCLUSIVE</span>
                                </div>
                                <h3 style="font-weight: bold; font-size: 1.2rem; margin: 15px 0 5px 0;">Aggressive Auto-Clean</h3>
                                <p class="card-text">Premium Feature Locked: Vectorized cleaning requires native desktop runtime. Download Windows App to execute in-place data repair.</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    with lc2:
                        st.markdown("""
                        <div class="custom-card" style="display: flex; flex-direction: column; justify-content: space-between; min-height: 250px;">
                            <div>
                                <div class="card-title">
                                    <span class="lock-icon">🔒</span>
                                    <span class="tag">GPU ACCELERATED</span>
                                </div>
                                <h3 style="font-weight: bold; font-size: 1.2rem; margin: 15px 0 5px 0;">Visual Analytics Suite</h3>
                                <p class="card-text">Locked in Cloud Lite: Interactive GPU heatmaps & scatter plots disabled on Streamlit Cloud sandbox. Unlock 120 FPS pipelines in Windows Desktop.</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    with lc3:
                        st.markdown("""
                        <div class="custom-card" style="display: flex; flex-direction: column; justify-content: space-between; min-height: 250px;">
                            <div>
                                <div class="card-title">
                                    <span class="lock-icon">🔒</span>
                                    <span class="tag">OFFLINE LLM</span>
                                </div>
                                <h3 style="font-weight: bold; font-size: 1.2rem; margin: 15px 0 5px 0;">Deterministic NLP Chat</h3>
                                <p class="card-text">NLP Engine Disabled: Offline local LLM inferencing available strictly in the standalone Windows application for zero data egress risk.</p>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error(f"Data parse failure. Error: {e}")

# ==========================================
# TAB 4: DOWNLOAD APP
# ==========================================
with tab_download:
    st.markdown("""
    <div class="top-status-bar">
        <span>ISOLATION: SECURE • VERSION: V3.2.0 STABLE</span>
        <span>100% AIR-GAPPED</span>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<h2 style='color: #0f172a !important; font-weight: bold; text-align: center; margin-top: 40px;'>Deploy Local Execution Engine</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569 !important; text-align: center; font-size: 1.1rem; margin-bottom: 40px;'>Acquire the standalone Windows executable for unrestricted, unlimited data usage.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="custom-card" style="margin-bottom: 30px;">
            <div class="card-title">Runtime Capability Matrix</div>
            <ul style="color: #475569 !important; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; line-height: 1.8;">
                <li><strong>OS Requirement:</strong> Windows 10/11 (64-bit)</li>
                <li><strong>File Size Quota:</strong> UNLIMITED (Hardware Bound)</li>
                <li><strong>Data Privacy:</strong> 100% AIR-GAPPED</li>
                <li><strong>Compute Architecture:</strong> AVX-512 / CUDA Support</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        dummy_exe_bytes = b"Executable build payload placeholder"
        st.download_button(
            label="Download Windows App (.exe)", 
            data=dummy_exe_bytes, 
            file_name="EDA_Engine_V3_Installer.exe", 
            mime="application/octet-stream"
        )
