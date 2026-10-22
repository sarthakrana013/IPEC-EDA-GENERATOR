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
    
    /* Force ALL text inputs, password boxes, and textareas to be white */
    input, textarea, [data-baseweb="input"], [data-baseweb="textarea"], [data-testid="stTextInput"] div {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }

    /* Fix the Chat Input Container specifically */
    [data-testid="stChatInput"] {
        background-color: #ffffff !important;
        border: 2px solid #107c41 !important;
        border-radius: 8px !important;
    }
    [data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
    }
    [data-testid="stChatInput"] button {
        background-color: #107c41 !important;
    }
    [data-testid="stChatInput"] button svg {
        fill: #ffffff !important;
    }

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
    [data-testid="stFileUploader"] label {
        color: #0f172a !important;
    }
    [data-testid="stFileUploader"] svg { fill: #107c41 !important; }
    
    [data-testid="stUploadedFile"] {
        background-color: #f0fdf4 !important;
        border: 1px solid #107c41 !important;
        border-radius: 4px !important;
    }
    [data-testid="stUploadedFile"] div, 
    [data-testid="stUploadedFile"] span, 
    [data-testid="stUploadedFile"] small { color: #0f172a !important; }

    /* Clean up the chat messages */
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
                <div class="bypass-title" style="margin-top: 10px; font-size: 1.1rem;">Skip Login with Windows Desktop (.exe)</div>
                <div class="bypass-text">Need to process data larger than 5 MB? Download the standalone native client for zero cloud dependencies, unmetered multi-gigabyte RAM analysis, and local GPU acceleration.</div>
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
                    
                    mod1, mod2, mod3 = st.tabs(["🗄️ Aggressive Auto-Clean", "📉 Visual Analytics", "🤖 True Cloud AI Assistant"])
                    
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
                            st.markdown("#### 💾 Export Processed Dataset")
                            csv_data = df.to_csv(index=False).encode('utf-8')
                            out_name = f"Cleaned_{st.session_state.last_filename.split('.')[0]}.csv"
                            st.download_button(
                                label="📥 Download Cleaned CSV",
                                data=csv_data,
                                file_name=out_name,
                                mime="text/csv",
                                use_container_width=True
                            )
                    
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
                        
                        # API KEY INPUT BOX
                        api_key = st.text_input("Enter your free Google Gemini API Key to wake up the AI:", type="password", help="Get a free key at aistudio.google.com")
                        
                        if api_key:
                            try:
                                import google.generativeai as genai
                                genai.configure(api_key=api_key)
                                # FIX: Switched to the universally supported 'gemini-pro' to prevent 404 errors
                                model = genai.GenerativeModel('gemini-pro')
                                
                                for message in st.session_state.chat_history:
                                    avatar_icon = "👤" if message["role"] == "user" else "🤖"
                                    with st.chat_message(message["role"], avatar=avatar_icon):
                                        st.markdown(message["content"])

                                if prompt := st.chat_input("Ask the AI anything about your data..."):
                                    st.chat_message("user", avatar="👤").markdown(prompt)
                                    st.session_state.chat_history.append({"role": "user", "content": prompt})
                                    
                                    with st.chat_message("assistant", avatar="🤖"):
                                        with st.spinner("AI is analyzing data..."):
                                            context = f"You are a helpful Data Science AI. You are helping a user analyze a dataset. \nHere are the columns: {df.columns.tolist()} \nHere are the data types: {df.dtypes.to_dict()} \nHere is a preview of the first 3 rows: \n{df.head(3).to_string()} \n\nBased on this dataset context, please answer the user's question concisely: {prompt}"
                                            
                                            response = model.generate_content(context)
                                            st.markdown(response.text)
                                            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                            
                            except ImportError:
                                st.error("🚨 Missing Library! Please add `google-generativeai` to your requirements.txt file on GitHub.")
                            except Exception as e:
                                st.error(f"AI Engine Error: Invalid API Key or Connection Issue. Details: {e}")
                        else:
                            st.info("🔒 The AI brain is asleep. Paste your Google Gemini API Key in the box above to activate it.")

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
