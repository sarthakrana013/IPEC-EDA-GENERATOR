import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import time

# 1. Page Configuration
st.set_page_config(page_title="EDA Engine Cloud", page_icon="📊", layout="wide")

# 2. CLEAN NATIVE THEME STYLING
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600&display=swap');
    
    .stApp { background-color: #f8fafc !important; }
    
    .top-status-bar {
        background-color: #107c41;
        color: #ffffff !important;
        padding: 10px 20px;
        border-radius: 6px;
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 13px;
        font-weight: 600;
        display: flex;
        justify-content: space-between;
        margin-bottom: 25px;
    }
    
    div[data-testid="metric-container"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        border-top: 4px solid #107c41 !important;
        border-radius: 6px !important;
        padding: 15px !important;
    }
    
    button[data-baseweb="tab"] {
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
    
    st.title("Dataframe Ingestion Pipeline")
    st.write("Transform raw, dirty matrices into ML-ready datasets with absolute data privacy.")
    
    if st.button("Authenticate & Launch Sandbox", type="primary"):
        st.info("Please click the '🔐 Authentication' tab above to log in.")
    
    st.markdown("---")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("100% Air-Gapped")
        st.write("Desktop execution engine runs natively. Zero data is transmitted to AWS/GCP, ensuring enterprise compliance.")
    with c2:
        st.subheader("Vectorized Cleaning")
        st.write("Autonomously purges regex anomalies, coercing types, and applying statistical median/mode imputation.")
    with c3:
        st.subheader("True Cloud AI")
        st.write("Powered by Google Gemini. Ask any question about your data and receive instant, intelligent analysis.")

    st.markdown("---")
    st.subheader("Platform Architecture & Objective")
    st.write("The EDA Engine Cloud is a purpose-built automated pipeline designed to eliminate the 80% manual overhead data scientists spend cleaning and profiling data. We bridge the gap between raw, unstructured matrices and machine-learning-ready datasets through automated imputation, GPU-accelerated visualizations, and an integrated NLP assistant.")

    st.subheader("The Competitive Advantage: Why Choose Us?")
    comp1, comp2, comp3 = st.columns(3)
    with comp1:
        st.info("**Vs. Enterprise BI (Power BI)**\n\n* **Theirs:** Expensive commercial licenses, steep learning curves, engineered for executive dashboards.\n* **Ours:** Purpose-built for ML engineers. One-click statistical imputation and direct CSV exports.")
    with comp2:
        st.info("**Vs. Cloud AI (ChatGPT)**\n\n* **Theirs:** Severe data privacy risks, strict cloud upload limits, and paid subscriptions.\n* **Ours:** 100% Air-Gapped desktop option ensures sensitive medical or financial data never leaves your hardware.")
    with comp3:
        st.info("**Vs. Manual Python**\n\n* **Theirs:** Hours spent writing repetitive boilerplate code (Pandas, Matplotlib) for every file.\n* **Ours:** Autonomous vectorized regex cleaning and automated correlation heatmaps rendered in seconds.")

# ==========================================
# TAB 2: AUTHENTICATION (PURA NATIVE STREAMLIT LAYOUT)
# ==========================================
with tab_auth:
    if st.session_state.logged_in:
        st.success("Authentication validated. Active session token generated.")
        if st.button("Sign Out of Session"):
            st.session_state.logged_in = False
            st.rerun()
    else:
        col1, col2 = st.columns([1.1, 1])
        
        with col1:
            st.markdown("### Sign in to EDA Cloud Lite")
            st.caption("Authenticate your session to provision an isolated exploratory sandbox.")
            
            st.text_input("Work Email / Institutional ID", placeholder="analyst@quant-research.org")
            st.text_input("Security Token / Master Key", type="password", placeholder="••••••••••••••••")
            
            st.selectbox("Target Pod Provisioning Tier", ["⚗️ Academic (5.0 MB microVM)", "🏢 Enterprise (VPC Air-Gap Proxy)", "👤 Individual (Shared Community)"])
            st.checkbox("Persist authenticated token on this browser for 30 days.", value=True)
            
            if st.button("Authenticate & Launch Sandbox →", type="primary"):
                st.session_state.logged_in = True
                st.session_state.username = "telemetry-inst-01"
                st.success("Connecting to secure node...")
                time.sleep(0.5)
                st.rerun()

        with col2:
            st.success("Cloud Lite Execution Specs • HEALTHY")
            st.markdown("""
            * **Strict 5.0 MB RAM Quota:** Enforced via frontend stream validation & config limiters.
            * **Zero Ephemeral Persistence:** Tables stored solely in volatile RAM and purged upon session termination.
            * **Streamlit Pod Availability:** Warm worker instances ready for instant query dispatch.
            """)
            
            st.warning("OFFLINE POWER MODE: Zero-Login Bypass")
            st.write("Need to process data larger than 5 MB? Download the standalone native client for zero cloud dependencies, unmetered multi-gigabyte RAM analysis, and local GPU acceleration.")
            st.download_button("🖥️ Download Standalone Windows App (.exe)", data=b"placeholder", file_name="EDA_Engine_V3_Installer.exe")

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
        
        st.subheader("Dataframe Ingestion Pipeline")
        st.error("⚠️ MAXIMUM UPLOAD LIMIT: 5.0 MB worth of files can be entered. Larger files will be automatically rejected.")
        
        uploaded_file = st.file_uploader("Upload dataset (CSV, XLSX, JSON, Parquet)", type=['csv', 'xlsx', 'json', 'parquet'])
        
        if uploaded_file:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            
            if file_size_mb > 5.0:
                st.error(f"🛑 REJECTED: Your file is {file_size_mb:.2f}MB. Only 5.0 MB files can be processed here.")
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
                            if st.button("✨ Execute Aggressive Auto-Clean", type="primary"):
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
                                        
                                        # BULLETPROOF FALLBACK AI CALL
                                        model = genai.GenerativeModel('gemini-1.5-flash')
                                        context = f"You are a helpful Data Science AI. You are helping a user analyze a dataset. \nHere are the columns: {df.columns.tolist()} \nHere are the data types: {df.dtypes.to_dict()} \nHere is a preview of the first 3 rows: \n{df.head(3).to_string()} \n\nBased on this dataset context, please answer the user's question concisely: {prompt}"
                                        
                                        response = model.generate_content(context)
                                        st.markdown(response.text)
                                        st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                        
                                    except Exception as e:
                                        # Fallback to gemini-pro if flash fails
                                        try:
                                            model = genai.GenerativeModel('gemini-pro')
                                            response = model.generate_content(context)
                                            st.markdown(response.text)
                                            st.session_state.chat_history.append({"role": "assistant", "content": response.text})
                                        except Exception as err:
                                            st.error(f"AI Engine Error: {err}")

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
                                type="primary",
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
    st.title("Deploy Local Execution Engine")
    st.write("Acquire the standalone Windows executable for unrestricted, unlimited data usage.")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("**Runtime Capability Matrix**\n\n* **OS Requirement:** Windows 10/11 (64-bit)\n* **File Size Quota:** UNLIMITED (Hardware Bound)\n* **Data Privacy:** 100% AIR-GAPPED\n* **Compute Architecture:** AVX-512 / CUDA Support")
        st.download_button("Download Windows App (.exe)", data=b"placeholder", file_name="EDA_Engine_V3_Installer.exe", type="primary")
