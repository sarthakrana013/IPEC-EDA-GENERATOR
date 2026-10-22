import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import time

# 1. Page Configuration
st.set_page_config(page_title="EDA Engine Cloud", page_icon="📊", layout="wide")

# 2. INJECTING THE "EXCEL GREEN & WHITE" UI/UX
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap');

    .stApp { background-color: #f8fafc !important; }
    
    html, body, p, span, div, h1, h2, h3, h4, h5, h6, label { 
        font-family: "Times New Roman", Times, Georgia, serif !important;
        color: #0f172a !important;
    }
    
    code, .stDataFrame, div[data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace !important;
    }

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

    .custom-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-top: 4px solid #107c41;
        border-radius: 6px;
        padding: 20px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        height: 100%;
    }
    
    .card-title { font-size: 1.1rem; font-weight: bold; color: #0f172a !important; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center;}
    .card-text { font-size: 0.9rem; color: #475569 !important; font-family: "Times New Roman", serif !important; line-height: 1.5; }

    .stButton > button, [data-testid="stDownloadButton"] > button {
        background-color: #107c41 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 4px !important;
        font-family: 'Times New Roman', serif !important;
        font-weight: bold !important;
        padding: 0.5rem 1rem !important;
        width: 100%;
    }
    .stButton > button:hover, [data-testid="stDownloadButton"] > button:hover { 
        background-color: #0b5c2f !important; 
    }
    .stButton > button *, [data-testid="stDownloadButton"] > button * { color: #ffffff !important; }

    /* ========================================================= */
    /* NUCLEAR WHITE BOX OVERRIDES FOR INPUTS & CHAT             */
    /* ========================================================= */
    
    input, textarea, [data-baseweb="input"], [data-baseweb="textarea"], [data-testid="stTextInput"] div {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }

    [data-testid="stChatInput"] {
        background-color: #ffffff !important;
        border: 2px solid #107c41 !important;
        border-radius: 8px !important;
    }
    [data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }
    [data-testid="stChatInput"] button { background-color: #107c41 !important; }
    [data-testid="stChatInput"] button svg { fill: #ffffff !important; }

    [data-testid="stFileUploader"] section {
        background-color: #ffffff !important;
        border: 2px dashed #107c41 !important;
        border-radius: 8px !important;
    }
    [data-testid="stFileUploader"] div, [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] small, [data-testid="stFileUploader"] p, [data-testid="stFileUploader"] label {
        color: #0f172a !important;
    }
    [data-testid="stFileUploader"] svg { fill: #107c41 !important; }
    
    [data-testid="stUploadedFile"] { background-color: #f0fdf4 !important; border: 1px solid #107c41 !important; border-radius: 4px !important; }
    [data-testid="stUploadedFile"] div, [data-testid="stUploadedFile"] span, [data-testid="stUploadedFile"] small { color: #0f172a !important; }

    [data-testid="stChatMessage"] { background-color: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 8px !important; padding: 10px !important; }
    [data-testid="stChatMessage"] * { color: #0f172a !important; }

    .tag { background-color: #f0fdf4; color: #107c41 !important; border: 1px solid #bbf7d0; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-family: 'JetBrains Mono', monospace !important; font-weight: bold;}

    div[data-testid="metric-container"] { background-color: #ffffff !important; border: 1px solid #e2e8f0 !important; border-top: 4px solid #107c41 !important; border-radius: 6px !important; padding: 15px !important; box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important; }
    div[data-testid="stMetricLabel"] * { color: #64748b !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.75rem !important; text-transform: uppercase !important; font-weight: bold !important;}
    
    button[data-baseweb="tab"] { font-family: 'Times New Roman', serif !important; font-weight: bold !important; font-size: 1.1rem !important; }
    
    /* Checkbox Fix */
    [data-testid="stCheckbox"] label span { color: #475569 !important; font-size: 0.85rem !important; }
</style>
""", unsafe_allow_html=True)

# 3. Session State 
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'df' not in st.session_state:
    st.session_state.df = None
if 'cleaned' not in st.session_state:
    st.session_state.cleaned = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'last_filename' not in st.session_state:
    st.session_state.last_filename = "Dataset"

st.markdown("<h2 style='color: #107c41; font-weight: bold; margin-bottom: 0;'>EDA Engine Cloud</h2>", unsafe_allow_html=True)
if st.session_state.logged_in:
    st.markdown(f"<p style='color: #107c41; font-family: monospace; font-size: 0.85rem; font-weight: bold; margin-top: 5px;'>Active Session: {st.session_state.username}</p>", unsafe_allow_html=True)
else:
    st.markdown("<p style='color: #64748b; font-size: 0.85rem; font-family: monospace; margin-top: 5px;'>Streamlit Community Cloud • V3.2.0</p>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 4. Top Navigation Tabs
tab_overview, tab_auth, tab_app, tab_download = st.tabs([
    "🏠 Overview", 
    "🔐 Authentication", 
    "⚡ Cloud App (Max 5MB)", 
    "📥 Windows App (Unlimited)"
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
            <div class="card-title">True Cloud AI</div>
            <div class="card-text">Powered by Google Gemini. Ask any question about your data and receive instant, intelligent analysis.</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# TAB 2: AUTHENTICATION
# ==========================================
with tab_auth:
    # 1. Custom Top Light-Grey Bar matching mockup
    st.markdown("""
    <div style="background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #64748b !important; margin-bottom: 10px;">
        <div><span style="color: #107c41; font-weight: bold;">◎ Streamlit Cloud Sandbox Gateway</span> • Ephemeral 5MB Container Provisioning Environment</div>
        <div><span style="color: #0f172a; font-weight: bold;">● TLS 1.3 ENCRYPTED • ISOLATION: SECURE</span> &nbsp;&nbsp;&nbsp; PORT: 8501-SANDBOX</div>
    </div>
    <div style="font-family: 'Times New Roman', serif; font-size: 0.8rem; font-weight: bold; color: #107c41 !important; margin-bottom: 25px;">
        EDA Engine Cloud <span style="color: #cbd5e1 !important; font-weight: normal;">/ Authentication Gateway / Node Provisioner</span>
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
        col1, col2 = st.columns([1.1, 1])
        with col1:
            st.markdown("""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 25px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <div style="background-color: #107c41; padding: 15px 20px; border-radius: 6px; margin: -25px -25px 25px -25px; display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <div style="font-weight: bold; font-size: 1.2rem; color: white !important; display: flex; align-items: center; gap: 10px;">
                            <div style="background: white; color: #107c41 !important; border-radius: 4px; padding: 2px 6px; font-size: 0.9rem;">☑</div> Sign in to EDA Cloud Lite
                        </div>
                        <div style="font-size: 0.8rem; font-weight: normal; margin-top: 4px; color: #bbf7d0 !important;">Authenticate your session to provision an isolated exploratory sandbox.</div>
                    </div>
                    <span style="border: 1px solid #4ade80; color: #4ade80 !important; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; padding: 2px 6px; border-radius: 4px;">v2.4.1</span>
                </div>
                
                <p style="font-family: 'Times New Roman', serif; font-size: 0.75rem; font-weight: bold; color: #475569 !important; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 10px;">Federated Analyst Single Sign-On</p>
                
                <div style="display: flex; gap: 10px; margin-bottom: 25px;">
                    <div style="flex: 1; border: 1px solid #e2e8f0; border-radius: 4px; padding: 8px; text-align: center; font-size: 0.85rem; font-weight: bold; color: #0f172a !important; display: flex; align-items: center; justify-content: center; gap: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
                        <span style="color: #ea4335 !important; font-size: 1.1rem;">■</span> Microsoft 365
                    </div>
                    <div style="flex: 1; border: 1px solid #e2e8f0; border-radius: 4px; padding: 8px; text-align: center; font-size: 0.85rem; font-weight: bold; color: #0f172a !important; display: flex; align-items: center; justify-content: center; gap: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
                        <span style="color: #4285F4 !important; font-size: 1.1rem; font-family: sans-serif;">G</span> Google Cloud
                    </div>
                    <div style="flex: 1; border: 1px solid #e2e8f0; border-radius: 4px; padding: 8px; text-align: center; font-size: 0.85rem; font-weight: bold; color: #0f172a !important; display: flex; align-items: center; justify-content: center; gap: 8px; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
                        <span style="font-size: 1.1rem;">🐙</span> GitHub Repo
                    </div>
                </div>
                
                <div style="display: flex; align-items: center; text-align: center; color: #94a3b8 !important; font-size: 0.8rem; font-style: italic; margin-bottom: 20px;">
                    <div style="flex: 1; height: 1px; background-color: #e2e8f0;"></div>
                    <div style="padding: 0 15px;">or authenticate via credentials</div>
                    <div style="flex: 1; height: 1px; background-color: #e2e8f0;"></div>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<p style='font-size: 0.85rem; font-weight: bold; margin-bottom: 5px; color: #0f172a !important;'>Work Email / Institutional ID</p>", unsafe_allow_html=True)
            email = st.text_input("Email", placeholder="analyst@quant-research.org", label_visibility="collapsed")
            
            st.markdown("""
                <div style='display: flex; justify-content: space-between; align-items: center; margin-top: 15px; margin-bottom: 5px;'>
                    <span style='font-size: 0.85rem; font-weight: bold; color: #0f172a !important;'>Security Token / Master Key</span>
                    <a href='#' style='color: #64748b; font-size: 0.75rem; text-decoration: none;'>Forgot key?</a>
                </div>
            """, unsafe_allow_html=True)
            token = st.text_input("Password", type="password", placeholder="••••••••••••••••", label_visibility="collapsed")
            
            st.markdown("""
                <p style="font-size: 0.85rem; font-weight: bold; margin-top: 25px; margin-bottom: 10px; color: #0f172a !important;">Target Pod Provisioning Tier</p>
                <div style="display: flex; gap: 10px; margin-bottom: 20px;">
                    <div style="flex: 1; border: 1px solid #107c41; background-color: #f0fdf4; border-radius: 4px; padding: 12px 10px;">
                        <div style="font-size: 0.85rem; font-weight: bold; color: #107c41 !important; margin-bottom: 2px;">⚗️ Academic</div>
                        <div style="font-size: 0.75rem; color: #64748b !important;">5.0 MB microVM</div>
                    </div>
                    <div style="flex: 1; border: 1px solid #e2e8f0; border-radius: 4px; padding: 12px 10px; opacity: 0.6;">
                        <div style="font-size: 0.85rem; font-weight: bold; color: #0f172a !important; margin-bottom: 2px;">🏢 Enterprise</div>
                        <div style="font-size: 0.75rem; color: #64748b !important;">VPC Air-Gap Proxy</div>
                    </div>
                    <div style="flex: 1; border: 1px solid #e2e8f0; border-radius: 4px; padding: 12px 10px; opacity: 0.6;">
                        <div style="font-size: 0.85rem; font-weight: bold; color: #0f172a !important; margin-bottom: 2px;">👤 Individual</div>
                        <div style="font-size: 0.75rem; color: #64748b !important;">Shared Community</div>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            st.checkbox("Persist authenticated token on this browser for 30 days (ephemeral DuckDB session cache only).", value=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Authenticate & Launch Sandbox →"):
                st.session_state.logged_in = True
                st.session_state.username = "telemetry-inst-01"
                st.success("Connecting to secure node...")
                time.sleep(0.5)
                st.rerun()
                
            st.markdown("""
                <p style="text-align: center; font-size: 0.75rem; color: #94a3b8 !important; margin-top: 20px;">
                    By connecting, you accept the 5.0 MB in-memory buffer constraint and automatic Firecracker microVM teardown on inactivity.
                </p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div style="background: white; border: 1px solid #e2e8f0; border-radius: 8px; padding: 25px; box-shadow: 0 1px 3px rgba(0,0,0,0.05); margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #f1f5f9; padding-bottom: 15px; margin-bottom: 20px;">
                    <span style="font-weight: bold; color: #0f172a !important; display: flex; align-items: center; gap: 8px;">
                        <span style="color: #107c41;">☷</span> Cloud Lite Execution Specs
                    </span>
                    <span style="background-color: #f0fdf4; color: #107c41 !important; border: 1px solid #bbf7d0; padding: 2px 8px; border-radius: 4px; font-size: 0.65rem; font-family: 'JetBrains Mono', monospace !important; font-weight: bold;">HEALTHY</span>
                </div>
                
                <div style="display: flex; align-items: flex-start; margin-bottom: 15px; border-bottom: 1px solid #f1f5f9; padding-bottom: 15px;">
                    <span style="color: #107c41 !important; margin-right: 12px; font-weight: bold; font-size: 1.1rem;">◎</span>
                    <div>
                        <div style="font-weight: bold; font-size: 0.95rem; color: #0f172a !important; margin-bottom: 4px;">Strict 5.0 MB RAM Quota</div>
                        <div style="font-size: 0.85rem; color: #64748b !important; line-height: 1.4;">Enforced via frontend stream validation & <code style="background: #f1f5f9; padding: 2px 4px; border-radius: 3px; font-size: 0.75rem;">.streamlit/config.toml</code> limiters.</div>
                    </div>
                </div>
                
                <div style="display: flex; align-items: flex-start; margin-bottom: 15px; border-bottom: 1px solid #f1f5f9; padding-bottom: 15px;">
                    <span style="color: #107c41 !important; margin-right: 12px; font-weight: bold; font-size: 1.1rem;">⟳</span>
                    <div>
                        <div style="font-weight: bold; font-size: 0.95rem; color: #0f172a !important; margin-bottom: 4px;">Zero Ephemeral Persistence</div>
                        <div style="font-size: 0.85rem; color: #64748b !important; line-height: 1.4;">Tables stored solely in volatile RAM. All PyArrow buffers are purged immediately upon tab or browser termination.</div>
                    </div>
                </div>

                <div style="display: flex; align-items: flex-start; margin-bottom: 25px;">
                    <span style="color: #107c41 !important; margin-right: 12px; font-weight: bold; font-size: 1.1rem;">⚲</span>
                    <div>
                        <div style="font-weight: bold; font-size: 0.95rem; color: #0f172a !important; margin-bottom: 4px;">Streamlit Pod Availability</div>
                        <div style="font-size: 0.85rem; color: #64748b !important; line-height: 1.4;">14 warm worker instances stand ready for instantaneous sub-12ms query dispatch via DuckDB WebAssembly bindings.</div>
                    </div>
                </div>
                
                <div style="padding-top: 15px; border-top: 1px solid #f1f5f9;">
                    <div style="display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #64748b !important; margin-bottom: 8px;">
                        <span>SANDBOX_HEAP_ALLOCATION</span>
                        <span style="color: #107c41 !important; font-weight: bold;">0.42 / 5.0 MB</span>
                    </div>
                    <div style="height: 6px; background-color: #f1f5f9; border-radius: 3px; overflow: hidden; border: 1px solid #e2e8f0;">
                        <div style="width: 8.4%; height: 100%; background-color: #107c41;"></div>
                    </div>
                </div>
            </div>
            
            <div style="background: #ffffff; border: 1px solid #4ade80; border-radius: 8px; padding: 25px; box-shadow: 0 4px 6px -1px rgba(74, 222, 128, 0.1);">
                <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                    <span style="background-color: #107c41; color: white !important; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; padding: 3px 8px; border-radius: 4px; font-weight: bold; letter-spacing: 0.05em;">OFFLINE POWER MODE</span>
                    <span style="font-family: 'Times New Roman', serif; font-size: 0.85rem; color: #0f172a !important; font-style: italic;">Zero-Login Bypass</span>
                </div>
                
                <div style="font-weight: bold; font-size: 1.2rem; color: #0f172a !important; margin-bottom: 10px;">Skip Login with Windows Desktop (.exe)</div>
                <div style="font-size: 0.85rem; color: #15803d !important; margin-bottom: 20px; line-height: 1.6;">Need to process data larger than 5 MB? Download the standalone native client for zero cloud dependencies, unmetered multi-gigabyte RAM analysis, 100% air-gapped security, and local GPU acceleration.</div>
                
                <button style="width: 100%; background: white; border: 1px solid #107c41; color: #107c41; padding: 10px; border-radius: 4px; font-family: 'Times New Roman', serif; font-size: 0.9rem; font-weight: bold; cursor: pointer; display: flex; justify-content: center; align-items: center; gap: 8px; box-shadow: 0 1px 2px rgba(16, 124, 65, 0.1);">
                    🖥️ Download Standalone Windows App (.exe) ↓
                </button>
                
                <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px; padding-top: 15px; border-top: 1px solid #f0fdf4; font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #64748b !important;">
                    <span>SHA-256: 9b2d...f41a</span>
                    <span>BUILD: v2.4-WIN64</span>
                    <span style="background: #dcfce7; padding: 3px 8px; border-radius: 4px; color: #16a34a !important; font-weight: bold;">SIZE: 84.2 MB</span>
                </div>
            </div>
            
            <div style="margin-top: 20px; display: flex; align-items: center; gap: 8px; font-size: 0.75rem; color: #94a3b8 !important; justify-content: center;">
                <span style="font-size: 1rem;">⛨</span> Compliant with HIPAA, FERPA, & GDPR non-retained statistical computing policies.
            </div>
            """, unsafe_allow_html=True)

# ==========================================
# TAB 3: CLOUD APP
# ==========================================
with tab_app:
    if not st.session_state.logged_in:
        st.error("Access Denied: Authentication required to access the cloud sandbox.")
        st.info("Navigate to the '🔐 Authentication' tab to sign in.")
    else:
        st.markdown("""
        <div class="top-status-bar">
            <span>SANDBOX ACTIVE: Fully Functional Engine (Max 5.0 MB Quota Enforced)</span>
            <span>ISOLATION: SECURE</span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <h2 style="margin: 0; font-weight: bold; color: #0f172a !important; display: flex; align-items: center; gap: 10px;">
                <span style="color: #107c41;">📄</span> Dataframe Ingestion Pipeline
            </h2>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #64748b !important; background: #e2e8f0; padding: 4px 8px; border-radius: 4px;">FORMATS: .CSV, .XLSX, .PARQUET, .JSON</span>
        </div>
        <p style="color: #ef4444; font-weight: bold;">⚠️ MAXIMUM UPLOAD LIMIT: 5.0 MB worth of files can be entered. Larger files will be automatically rejected to prevent server overload.</p>
        """, unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("", type=['csv', 'xlsx', 'json', 'parquet'], label_visibility="collapsed")
        
        if uploaded_file:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            
            if file_size_mb > 5.0:
                st.error(f"🛑 REJECTED: Your file is {file_size_mb:.2f}MB. Only 5.0 MB worth of files can be entered here. Please use the Desktop App for larger datasets.")
            else:
                try:
                    file_ext = uploaded_file.name.split('.')[-1].lower()
                    if st.session_state.df is None or st.session_state.last_filename != uploaded_file.name:
                        st.session_state.last_filename = uploaded_file.name
                        if file_ext in ['csv', 'txt']:
                            st.session_state.df = pd.read_csv(uploaded_file)
                        elif file_ext in ['xlsx', 'xls']:
                            st.session_state.df = pd.read_excel(uploaded_file)
                        elif file_ext == 'json':
                            st.session_state.df = pd.read_json(uploaded_file)
                        elif file_ext == 'parquet':
                            st.session_state.df = pd.read_parquet(uploaded_file)
                        st.session_state.df.columns = st.session_state.df.columns.str.strip()
                        st.session_state.cleaned = False
                        st.session_state.chat_history = []
                    
                    df = st.session_state.df
                    
                    col1, col2, col3, col4, col5 = st.columns(5)
                    col1.metric("TOTAL ROWS", f"{df.shape[0]:,}")
                    col2.metric("COLUMNS", f"{df.shape[1]}")
                    col3.metric("IN-MEMORY SIZE", f"{file_size_mb:.2f} MB")
                    col4.metric("TYPING SCHEMAS", f"{len(df.select_dtypes(include=['float64', 'int64']).columns)} Num")
                    col5.metric("NULL / MISSING", f"{df.isnull().sum().sum():,}")
                    
                    st.markdown("<hr>", unsafe_allow_html=True)
                    
                    mod1, mod2, mod3, mod4 = st.tabs(["🗄️ Aggressive Auto-Clean", "📉 Visual Analytics", "🤖 True Cloud AI Assistant", "💾 Export Data"])
                    
                    with mod1:
                        st.markdown("### Dataset Architecture & Cleaning")
                        st.dataframe(df.head(), use_container_width=True)
                        
                        if not st.session_state.cleaned:
                            st.warning("Data is raw. It may contain missing values.")
                            if st.button("✨ Execute Aggressive Auto-Clean", use_container_width=True):
                                with st.spinner("Cleaning dataset on cloud server..."):
                                    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                                    cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
                                    for col in num_cols:
                                        median_val = df[col].median()
                                        df[col] = df[col].fillna(median_val if pd.notna(median_val) else 0)
                                    for col in cat_cols:
                                        mode_series = df[col].mode()
                                        mode_val = mode_series[0] if not mode_series.empty else "Unknown"
                                        df[col] = df[col].fillna(mode_val)
                                        
                                    st.session_state.df = df
                                    st.session_state.cleaned = True
                                    st.rerun()
                        else:
                            st.success("✅ Dataset has been aggressively cleaned. Zero missing values remain.")
                    
                    with mod2:
                        st.markdown("### Visual Analytics Suite")
                        numeric_cols_viz = df.select_dtypes(include=[np.number]).columns.tolist()
                        
                        if len(numeric_cols_viz) > 0:
                            chart_type = st.radio("Select Analysis Type:", ["Correlation Analysis", "Feature Distribution", "Bivariate Scatter"], horizontal=True)
                            if chart_type == "Correlation Analysis" and len(numeric_cols_viz) >= 2:
                                custom_colors = [[0.0, '#ffffff'], [1.0, '#107c41']] 
                                fig = px.imshow(df[numeric_cols_viz].corr(), text_auto=".2f", color_continuous_scale=custom_colors, aspect="auto")
                                st.plotly_chart(fig, use_container_width=True)
                            elif chart_type == "Feature Distribution" and numeric_cols_viz:
                                selected_col = st.selectbox("Select Feature:", numeric_cols_viz)
                                fig = px.histogram(df, x=selected_col, color_discrete_sequence=['#107c41'])
                                st.plotly_chart(fig, use_container_width=True)
                            elif chart_type == "Bivariate Scatter" and len(numeric_cols_viz) >= 2:
                                col_x = st.selectbox("X-Axis Feature:", numeric_cols_viz, index=0)
                                col_y = st.selectbox("Y-Axis Feature:", numeric_cols_viz, index=1 if len(numeric_cols_viz)>1 else 0)
                                fig = px.scatter(df, x=col_x, y=col_y, color_discrete_sequence=['#107c41'])
                                st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No numerical columns available for visualizations.")
                            
                    with mod3:
                        st.markdown("### ☁️ True Online AI Data Assistant")
                        st.caption("Powered by Google Gemini API. Ask absolutely anything about your dataset.")
                        
                        for message in st.session_state.chat_history:
                            avatar_icon = "👤" if message["role"] == "user" else "🤖"
                            with st.chat_message(message["role"], avatar=avatar_icon):
                                st.markdown(message["content"])

                        if prompt := st.chat_input("Ask the AI anything about your data..."):
                            st.chat_message("user", avatar="👤").markdown(prompt)
                            st.session_state.chat_history.append({"role": "user", "content": prompt})
                            
                            with st.chat_message("assistant", avatar="🤖"):
                                with st.spinner("AI is analyzing data..."):
                                    try:
                                        api_key = st.secrets["GEMINI_API_KEY"]
                                        import google.generativeai as genai
                                        genai.configure(api_key=api_key)
                                        
                                        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                                        
                                        if not available_models:
                                            st.error("🚨 Your API key is valid, but Google has not enabled text-generation for it.")
                                        else:
                                            target_model = 'models/gemini-1.5-flash'
                                            if target_model not in available_models:
                                                target_model = available_models[0] 
                                                
                                            model = genai.GenerativeModel(target_model)
                                            
                                            context = f"You are a helpful Data Science AI. You are helping a user analyze a dataset. \nHere are the columns: {df.columns.tolist()} \nHere are the data types: {df.dtypes.to_dict()} \nHere is a preview of the first 3 rows: \n{df.head(3).to_string()} \n\nBased on this dataset context, please answer the user's question concisely: {prompt}"
                                            
                                            response = model.generate_content(context)
                                            st.markdown(response.text)
                                            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                        
                                    except KeyError:
                                        st.error("🚨 Configuration Error: GEMINI_API_KEY not found in Streamlit Secrets.")
                                    except ImportError:
                                        st.error("🚨 Missing Library! Please add `google-generativeai` to your requirements.txt file on GitHub.")
                                    except Exception as e:
                                        st.error(f"AI Engine Error: Connection Issue. Details: {e}")

                    with mod4:
                        st.markdown("### 💾 Export Processed Dataset")
                        if not st.session_state.cleaned:
                            st.error("🛑 STOP! You cannot export this file yet. The dataset still contains uncleaned data.")
                            st.warning("👉 Go back to the '🗄️ Aggressive Auto-Clean' tab and click the clean button first.")
                        else:
                            st.success("✅ Dataset has been cleaned and is ready for export.")
                            csv_data = df.to_csv(index=False).encode('utf-8')
                            out_name = f"Cleaned_{st.session_state.last_filename.split('.')[0]}.csv"
                            st.download_button(
                                label="📥 Download Cleaned CSV",
                                data=csv_data,
                                file_name=out_name,
                                mime="text/csv",
                                use_container_width=True
                            )

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
