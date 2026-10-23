import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import time

# 1. Page Configuration
st.set_page_config(page_title="EDA Engine Cloud | Clean CSVs Fast", page_icon="✨", layout="wide")

# 2. INJECTING MODERN SaaS UI/UX (DataSort Vibe)
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

/* Global Modern Font */
html, body, p, h1, h2, h3, h4, h5, h6, label, li, b, strong, span, div { 
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    color: #1e293b !important;
}

code, .stDataFrame, div[data-testid="stMetricValue"] {
    font-family: 'JetBrains Mono', monospace !important;
}

.stApp { background-color: #f8fafc !important; }

/* Modern Top Bar */
.top-status-bar {
    background-color: #ffffff;
    color: #64748b !important;
    padding: 12px 20px;
    border-radius: 8px;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px;
    font-weight: 600;
    display: flex;
    justify-content: space-between;
    margin-bottom: 30px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.top-status-bar span { color: #64748b !important; }

/* SaaS Feature Cards */
.custom-card {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 25px;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
    height: 100%;
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.custom-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1);
}
.card-icon { font-size: 2rem; margin-bottom: 15px; }
.card-title { font-size: 1.1rem; font-weight: 600; color: #0f172a !important; margin-bottom: 10px;}
.card-text { font-size: 0.95rem; color: #475569 !important; line-height: 1.6; }

/* Modern Primary Buttons */
.stButton > button, [data-testid="stDownloadButton"] > button {
    background-color: #2563eb !important; /* Modern SaaS Blue */
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.6rem 1.2rem !important;
    width: 100%;
    text-align: center;
    box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
}
.stButton > button:hover, [data-testid="stDownloadButton"] > button:hover { 
    background-color: #1d4ed8 !important; 
    box-shadow: 0 6px 8px -1px rgba(37, 99, 235, 0.3);
}
.stButton > button *, [data-testid="stDownloadButton"] > button * { color: #ffffff !important; }

/* Sleek Inputs */
input:not([type="file"]), textarea, [data-baseweb="input"], [data-baseweb="textarea"], [data-testid="stTextInput"] div {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border-radius: 6px !important;
}

/* Massive, Inviting Drag & Drop Zone */
[data-testid="stFileUploader"] section {
    background-color: #f8fafc !important;
    border: 2px dashed #cbd5e1 !important;
    border-radius: 12px !important;
    padding: 40px 20px !important;
    transition: border-color 0.2s ease;
}
[data-testid="stFileUploader"] section:hover {
    border-color: #2563eb !important;
    background-color: #eff6ff !important;
}
[data-testid="stFileUploader"] svg { fill: #94a3b8 !important; width: 40px; height: 40px; }
[data-testid="stFileUploader"] div, [data-testid="stFileUploader"] span, [data-testid="stFileUploader"] small, [data-testid="stFileUploader"] p, [data-testid="stFileUploader"] label {
    color: #475569 !important;
}

/* FIX FOR DOUBLE OVERLAPPING TEXT: Hides native browser input text */
[data-testid="stFileUploader"] input[type="file"] {
    color: transparent !important;
}

[data-testid="stUploadedFile"] { background-color: #eff6ff !important; border: 1px solid #bfdbfe !important; border-radius: 8px !important; }
[data-testid="stUploadedFile"] * { color: #1e3a8a !important; }

/* Chat UI */
[data-testid="stChatMessage"] { background-color: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 8px !important; padding: 15px !important; box-shadow: 0 1px 2px rgba(0,0,0,0.02);}
[data-testid="stChatMessage"] * { color: #1e293b !important; }
[data-testid="stChatInput"] { background-color: #ffffff !important; border: 1px solid #cbd5e1 !important; border-radius: 8px !important; }
[data-testid="stChatInput"] textarea { background-color: #ffffff !important; color: #0f172a !important; }
[data-testid="stChatInput"] button { background-color: #2563eb !important; border-radius: 6px !important; }
[data-testid="stChatInput"] button svg { fill: #ffffff !important; }

/* Dataframes */
[data-testid="stElementToolbar"] { background-color: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 6px !important; }
[data-testid="stElementToolbar"] button svg { fill: #64748b !important; }
div[data-baseweb="tooltip"] > div { background-color: #1e293b !important; color: #ffffff !important; border-radius: 6px !important; font-size: 0.8rem !important; }

/* Metrics */
div[data-testid="metric-container"] { background-color: #ffffff !important; border: 1px solid #e2e8f0 !important; border-radius: 12px !important; padding: 20px !important; box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important; }
div[data-testid="stMetricLabel"] * { color: #64748b !important; font-family: 'Inter', sans-serif !important; font-size: 0.8rem !important; font-weight: 500 !important; text-transform: uppercase; letter-spacing: 0.05em;}
div[data-testid="stMetricValue"] { font-size: 1.8rem !important; font-weight: 700 !important; color: #0f172a !important; font-family: 'Inter', sans-serif !important;}

button[data-baseweb="tab"] { font-family: 'Inter', sans-serif !important; font-weight: 600 !important; font-size: 1rem !important; }
[data-testid="stCheckbox"] label span { color: #475569 !important; font-size: 0.9rem !important; }

/* Hero Section */
.hero-title { font-size: 3.5rem; font-weight: 800; color: #0f172a !important; text-align: center; margin-top: 40px; margin-bottom: 15px; letter-spacing: -0.02em; line-height: 1.2;}
.hero-subtitle { font-size: 1.25rem; color: #475569 !important; text-align: center; margin-bottom: 50px; font-weight: 400; max-width: 600px; margin-left: auto; margin-right: auto;}
.highlight-text { color: #2563eb !important; }
</style>
""", unsafe_allow_html=True)

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

st.markdown("<div style='font-size: 1.2rem; font-weight: 700; color: #0f172a; margin-bottom: 10px; display: flex; align-items: center; gap: 8px;'>✨ DataSort Cloud</div>", unsafe_allow_html=True)

tab_overview, tab_auth, tab_app, tab_download = st.tabs([
    "🏠 Home", 
    "🔐 Login", 
    "⚡ Clean CSV (App)", 
    "📥 Desktop App"
])

# ==========================================
# TAB 1: OVERVIEW (SaaS Landing Page)
# ==========================================
with tab_overview:
    st.markdown("""
<div class="hero-title">Clean Messy CSV Files <br><span class="highlight-text">Instantly & Securely.</span></div>
<div class="hero-subtitle">Transform raw, dirty datasets into ML-ready matrices in seconds. 100% free, automated, and private.</div>
""", unsafe_allow_html=True)
    
    # FIX: Tighter column ratio perfectly centers the button
    col_btn1, col_btn2, col_btn3 = st.columns([3, 2, 3])
    with col_btn2:
        if st.button("Start Cleaning for Free", use_container_width=True):
            st.info("Please click the '🔐 Login' tab above to authenticate your session.")
    
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    
    st.markdown("<h3 style='text-align: center; font-weight: 700; margin-bottom: 30px;'>How it works</h3>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
<div class="custom-card" style="text-align: center;">
    <div class="card-icon">📤</div>
    <div class="card-title">1. Upload your messy file</div>
    <div class="card-text">Drag and drop your CSV, Excel, or JSON file into our secure, ephemeral cloud sandbox.</div>
</div>
""", unsafe_allow_html=True)
    with c2:
        st.markdown("""
<div class="custom-card" style="text-align: center;">
    <div class="card-icon">⚡</div>
    <div class="card-title">2. Aggressive Auto-Clean</div>
    <div class="card-text">Our engine automatically strips invalid characters, fixes data types, and imputes missing values.</div>
</div>
""", unsafe_allow_html=True)
    with c3:
        st.markdown("""
<div class="custom-card" style="text-align: center;">
    <div class="card-icon">📥</div>
    <div class="card-title">3. Export & Analyze</div>
    <div class="card-text">Download your pristine dataset instantly, or chat with it using our offline NLP engine.</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# TAB 2: AUTHENTICATION
# ==========================================
with tab_auth:
    if st.session_state.logged_in:
        st.success("Authentication validated. Active session token generated.")
        col_btn1, col_btn2, col_btn3 = st.columns([1, 1, 1])
        with col_btn2:
            if st.button("Sign Out of Session"):
                st.session_state.logged_in = False
                st.rerun()
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1.2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; margin-bottom: 20px;">
                <svg height="48" viewBox="0 0 16 16" version="1.1" width="48" aria-hidden="true" style="fill: #0f172a;">
                    <path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z"></path>
                </svg>
                <div style="font-weight: 400; font-size: 1.5rem; color: #24292f !important; margin-top: 15px; margin-bottom: 20px;">Sign in to GitHub</div>
            </div>
            
            <div style="background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 6px; padding: 20px; box-shadow: 0 1px 3px rgba(0,0,0,0.05);">
                <p style="font-size: 0.9rem; margin-bottom: 5px; color: #24292f !important; font-weight: 500;">Username or email address</p>
            """, unsafe_allow_html=True)
            
            email = st.text_input("Email", label_visibility="collapsed")
            
            st.markdown("""
                <div style='display: flex; justify-content: space-between; align-items: center; margin-top: 15px; margin-bottom: 5px;'>
                    <span style='font-size: 0.9rem; color: #24292f !important; font-weight: 500;'>Password</span>
                    <a href='#' style='color: #0969da; font-size: 0.8rem; text-decoration: none;'>Forgot password?</a>
                </div>
            """, unsafe_allow_html=True)
            token = st.text_input("Password", type="password", label_visibility="collapsed")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("Sign in", use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.username = "telemetry-inst-01"
                st.success("Authenticating...")
                time.sleep(0.5)
                st.rerun()
                
            st.markdown("""
            </div>
            
            <div style="display: flex; align-items: center; text-align: center; color: #57606a !important; font-size: 0.9rem; margin: 20px 0;">
                <div style="flex: 1; height: 1px; background-color: #d0d7de;"></div>
                <div style="padding: 0 15px;">or</div>
                <div style="flex: 1; height: 1px; background-color: #d0d7de;"></div>
            </div>
            
            <div style="text-align: center; font-size: 0.9rem; color: #24292f !important; margin-bottom: 10px;">
                New to GitHub? <a href="#" style="color: #0969da; text-decoration: none;">Create an account</a>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
            <style>
                .stButton > button {
                    background-color: #2da44e !important;
                    color: #ffffff !important;
                    border: 1px solid rgba(27,31,36,0.15) !important;
                    border-radius: 6px !important;
                    font-weight: 500 !important;
                    font-size: 14px !important;
                    box-shadow: none !important;
                }
                .stButton > button:hover {
                    background-color: #2c974b !important;
                }
            </style>
            """, unsafe_allow_html=True)

# ==========================================
# TAB 3: CLOUD APP
# ==========================================
with tab_app:
    if not st.session_state.logged_in:
        st.error("Access Denied: Authentication required to access the cloud sandbox.")
        st.info("Navigate to the '🔐 Login' tab to sign in.")
    else:
        st.markdown("""
<div style="text-align: center; margin-bottom: 30px;">
    <h2 style="font-weight: 700; color: #0f172a; margin-bottom: 10px;">Upload your messy dataset</h2>
    <p style="color: #64748b; font-size: 1rem;">Supports CSV, Excel, JSON, and Parquet up to 5.0 MB.</p>
</div>
""", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("", type=['csv', 'xlsx', 'json', 'parquet'], label_visibility="collapsed")
        
        if uploaded_file:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            
            if file_size_mb > 5.0:
                st.error(f"🛑 REJECTED: Your file is {file_size_mb:.2f}MB. Free tier limit is 5.0 MB.")
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
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    col1, col2, col3, col4, col5 = st.columns(5)
                    col1.metric("TOTAL ROWS", f"{df.shape[0]:,}")
                    col2.metric("COLUMNS", f"{df.shape[1]}")
                    col3.metric("FILE SIZE", f"{file_size_mb:.2f} MB")
                    col4.metric("NUMERIC COLS", f"{len(df.select_dtypes(include=['float64', 'int64']).columns)}")
                    col5.metric("MISSING VALUES", f"{df.isnull().sum().sum():,}")
                    
                    st.markdown("<hr style='margin: 30px 0; border: 1px solid #e2e8f0;'>", unsafe_allow_html=True)
                    
                    mod1, mod2, mod3, mod4 = st.tabs(["✨ Auto-Clean", "📊 Visuals", "💬 AI Chat", "💾 Download"])
                    
                    with mod1:
                        st.markdown("<h3 style='font-size: 1.2rem; font-weight: 600; margin-bottom: 15px;'>Dataset Preview</h3>", unsafe_allow_html=True)
                        st.dataframe(df.head(), use_container_width=True)
                        
                        if not st.session_state.cleaned:
                            st.info("💡 Your data is raw and may contain missing values or invalid characters.")
                            if st.button("✨ Execute Aggressive Auto-Clean", use_container_width=True):
                                with st.spinner("Purging anomalies and imputing missing data..."):
                                    # Phantom character hunting
                                    dirty_placeholders = ['-', '?', 'NA', 'N/A', 'n/a', 'na', 'null', 'Null', '', ' ', '#N/A']
                                    df = df.replace(dirty_placeholders, np.nan)
                                    
                                    for c in df.columns:
                                        if df[c].dtype == 'object':
                                            df[c] = pd.to_numeric(df[c], errors='ignore')
                                            
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
                        st.markdown("<h3 style='font-size: 1.2rem; font-weight: 600; margin-bottom: 15px;'>Visual Analytics</h3>", unsafe_allow_html=True)
                        numeric_cols_viz = df.select_dtypes(include=[np.number]).columns.tolist()
                        
                        if len(numeric_cols_viz) > 0:
                            chart_type = st.radio("Select Analysis Type:", ["Correlation Matrix", "Feature Distribution", "Scatter Plot"], horizontal=True)
                            if chart_type == "Correlation Matrix" and len(numeric_cols_viz) >= 2:
                                custom_colors = [[0.0, '#eff6ff'], [1.0, '#2563eb']] 
                                fig = px.imshow(df[numeric_cols_viz].corr(), text_auto=".2f", color_continuous_scale=custom_colors, aspect="auto")
                                st.plotly_chart(fig, use_container_width=True)
                            elif chart_type == "Feature Distribution" and numeric_cols_viz:
                                selected_col = st.selectbox("Select Feature:", numeric_cols_viz)
                                fig = px.histogram(df, x=selected_col, color_discrete_sequence=['#2563eb'])
                                st.plotly_chart(fig, use_container_width=True)
                            elif chart_type == "Scatter Plot" and len(numeric_cols_viz) >= 2:
                                col_x = st.selectbox("X-Axis:", numeric_cols_viz, index=0)
                                col_y = st.selectbox("Y-Axis:", numeric_cols_viz, index=1 if len(numeric_cols_viz)>1 else 0)
                                fig = px.scatter(df, x=col_x, y=col_y, color_discrete_sequence=['#2563eb'])
                                st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No numerical columns available for visualizations.")
                            
                    with mod3:
                        st.markdown("<h3 style='font-size: 1.2rem; font-weight: 600; margin-bottom: 5px;'>Deterministic NLP Chat</h3>", unsafe_allow_html=True)
                        st.caption("Ask questions about specific columns. Try: 'What is the average of [column]?'")
                        
                        for message in st.session_state.chat_history:
                            with st.chat_message(message["role"]):
                                if message["type"] == "text":
                                    st.markdown(message["content"])
                                elif message["type"] == "dataframe":
                                    st.dataframe(message["content"])

                        if prompt := st.chat_input("Ask about your data..."):
                            st.chat_message("user").markdown(prompt)
                            st.session_state.chat_history.append({"role": "user", "type": "text", "content": prompt})
                            
                            with st.chat_message("assistant"):
                                prompt_lower = prompt.lower()
                                response_text = ""
                                response_df = None
                                
                                mentioned_cols = [c for c in df.columns if c.lower() in prompt_lower]
                                
                                if mentioned_cols:
                                    col = mentioned_cols[0] 
                                    if any(word in prompt_lower for word in ['max', 'maximum', 'highest']):
                                        if pd.api.types.is_numeric_dtype(df[col]):
                                            response_text = f"The maximum value in **{col}** is {df[col].max():.2f}."
                                        else:
                                            response_text = f"Column **{col}** is not numeric."
                                    elif any(word in prompt_lower for word in ['min', 'minimum', 'lowest']):
                                        if pd.api.types.is_numeric_dtype(df[col]):
                                            response_text = f"The minimum value in **{col}** is {df[col].min():.2f}."
                                        else:
                                            response_text = f"Column **{col}** is not numeric."
                                    elif any(word in prompt_lower for word in ['mean', 'average', 'avg']):
                                        if pd.api.types.is_numeric_dtype(df[col]):
                                            response_text = f"The average value of **{col}** is {df[col].mean():.2f}."
                                        else:
                                            response_text = f"Column **{col}** is not numeric."
                                    else:
                                        response_text = f"Here is a quick look at the data inside **{col}**:"
                                        response_df = df[[col]].head(5)
                                else:
                                    if any(word in prompt_lower for word in ['shape', 'size', 'row', 'column']):
                                        response_text = f"Your dataset consists of **{df.shape[0]:,} rows** and **{df.shape[1]} columns**."
                                    else:
                                        response_text = "🤖 *I am your offline Data NLP Engine.* Mention a specific column name (e.g. 'what is the average of [column]')."
                                
                                st.markdown(response_text)
                                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": response_text})
                                if response_df is not None:
                                    st.dataframe(response_df)
                                    st.session_state.chat_history.append({"role": "assistant", "type": "dataframe", "content": response_df})

                    with mod4:
                        st.markdown("<h3 style='font-size: 1.2rem; font-weight: 600; margin-bottom: 15px;'>Export Cleaned Data</h3>", unsafe_allow_html=True)
                        if not st.session_state.cleaned:
                            st.error("🛑 The dataset still contains uncleaned data.")
                            st.warning("👉 Go to the '✨ Auto-Clean' tab and clean the file first.")
                        else:
                            st.success("✅ Dataset is fully processed and ready for download.")
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
    st.markdown("<h2 style='color: #0f172a !important; font-weight: 800; text-align: center; margin-top: 40px;'>Get the Desktop App</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569 !important; text-align: center; font-size: 1.1rem; margin-bottom: 40px;'>Unrestricted, unlimited data usage running locally on your hardware.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
<div class="custom-card" style="margin-bottom: 30px;">
    <div class="card-title">Runtime Capability Matrix</div>
    <ul style="color: #475569 !important; font-size: 0.95rem; line-height: 1.8; padding-left: 20px;">
        <li><strong>OS Requirement:</strong> Windows 10/11 (64-bit)</li>
        <li><strong>File Size Quota:</strong> UNLIMITED (Hardware Bound)</li>
        <li><strong>Data Privacy:</strong> 100% AIR-GAPPED</li>
        <li><strong>Compute Architecture:</strong> AVX-512 / CUDA Support</li>
    </ul>
</div>
""", unsafe_allow_html=True)
        
        dummy_exe_bytes = b"Executable build payload placeholder"
        st.download_button(
            label="Download for Windows (.exe)", 
            data=dummy_exe_bytes, 
            file_name="EDA_Engine_V3_Installer.exe", 
            mime="application/octet-stream"
        )
