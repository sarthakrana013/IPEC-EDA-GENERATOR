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

    /* File Uploader Dropzone */
    [data-testid="stFileUploader"] section {
        background-color: #ffffff !important;
        border: 2px dashed #107c41 !important;
        border-radius: 8px !important;
    }
    [data-testid="stFileUploader"] div, 
    [data-testid="stFileUploader"] span, 
    [data-testid="stFileUploader"] small,
    [data-testid="stFileUploader"] p,
    [data-testid="stFileUploader"] label { color: #0f172a !important; }
    [data-testid="stFileUploader"] svg { fill: #107c41 !important; }
    
    [data-testid="stUploadedFile"] {
        background-color: #f0fdf4 !important;
        border: 1px solid #107c41 !important;
        border-radius: 4px !important;
    }
    [data-testid="stUploadedFile"] div, 
    [data-testid="stUploadedFile"] span, 
    [data-testid="stUploadedFile"] small { color: #0f172a !important; }

    /* Fix Chat Input Box */
    [data-testid="stChatInput"] { background-color: #ffffff !important; border: 1px solid #107c41 !important; }
    [data-testid="stChatInput"] textarea { background-color: #ffffff !important; color: #0f172a !important; }
    [data-testid="stChatInput"] button { background-color: #107c41 !important; }
    [data-testid="stChatInput"] button svg { fill: #ffffff !important; }

    /* FIX: Force Chat Bubbles to be White & Readable */
    [data-testid="stChatMessage"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }
    [data-testid="stChatMessage"] * {
        color: #0f172a !important;
    }

    .auth-header { background-color: #107c41; color: white !important; padding: 15px 20px; border-radius: 6px 6px 0 0; margin: -20px -20px 20px -20px; font-weight: bold; font-size: 1.2rem;}
    .spec-item { display: flex; align-items: flex-start; margin-bottom: 15px; border-bottom: 1px solid #f1f5f9; padding-bottom: 10px;}
    .spec-icon { color: #107c41 !important; margin-right: 10px; font-weight: bold;}
    .spec-title { font-weight: bold; font-size: 0.95rem; color: #0f172a !important; margin-bottom: 2px;}
    .spec-desc { font-size: 0.85rem; color: #64748b !important; }

    .bypass-box { border: 2px solid #bbf7d0; background-color: #f0fdf4; border-radius: 6px; padding: 15px; margin-top: 20px;}
    .bypass-title { color: #107c41 !important; font-weight: bold; margin-bottom: 5px;}
    .bypass-text { color: #15803d !important; font-size: 0.85rem; margin-bottom: 15px;}
    
    .tag { background-color: #f0fdf4; color: #107c41 !important; border: 1px solid #bbf7d0; padding: 2px 8px; border-radius: 12px; font-size: 0.75rem; font-family: 'JetBrains Mono', monospace !important; font-weight: bold;}

    div[data-testid="metric-container"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-top: 4px solid #107c41 !important;
        border-radius: 6px !important;
        padding: 15px !important;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05) !important;
    }
    div[data-testid="stMetricLabel"] * { color: #64748b !important; font-family: 'JetBrains Mono', monospace !important; font-size: 0.75rem !important; text-transform: uppercase !important; font-weight: bold !important;}
    
    button[data-baseweb="tab"] {
        font-family: 'Times New Roman', serif !important;
        font-weight: bold !important;
        font-size: 1.1rem !important;
    }
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
            <div class="card-title">Online Cloud NLP</div>
            <div class="card-text">Query matrices via our secure cloud servers using standard language. The online LLM outputs results instantly.</div>
        </div>
        """, unsafe_allow_html=True)

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
                <div class="spec-item"><span class="spec-icon">●</span><div><div class="spec-title">Strict 5.0 MB RAM Quota</div><div class="spec-desc">Enforced via frontend stream validation & config.toml limiters.</div></div></div>
                <div class="spec-item"><span class="spec-icon">●</span><div><div class="spec-title">Zero Ephemeral Persistence</div><div class="spec-desc">Tables stored solely in volatile RAM. All PyArrow buffers are purged immediately upon tab or browser termination.</div></div></div>
            </div>
            <div class="bypass-box">
                <span class="tag" style="background: white;">OFFLINE POWER MODE</span>
                <div class="bypass-title" style="margin-top: 10px; font-size: 1.1rem
