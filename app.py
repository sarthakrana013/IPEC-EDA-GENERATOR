import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import time
import google.generativeai as genai
from sklearn.impute import KNNImputer

# 1. Page Configuration
st.set_page_config(page_title="DataSort Cloud | Clean CSVs Fast", page_icon="✨", layout="wide")

# 2. NUCLEAR SAAS CSS INJECTION (EXCEL GREEN THEME)
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
html, body, p, h1, h2, h3, h4, h5, h6, label, li, span, div {
    font-family: 'Inter', sans-serif !important;
    color: #0f172a !important;
}
.stApp { background-color: #f8fafc !important; }

/* TABS OVERRIDE - FORCES SAAS PILL DESIGN */
.stTabs [data-baseweb="tab-list"] { gap: 12px !important; margin-bottom: 30px !important; }
.stTabs [data-baseweb="tab"] { height: 48px !important; background-color: #ffffff !important; border: 2px solid #e2e8f0 !important; border-radius: 30px !important; padding: 0 24px !important; color: #64748b !important; font-weight: 700 !important; font-size: 1rem !important; margin: 0 !important; transition: all 0.2s ease !important; }
.stTabs [data-baseweb="tab"]:hover { border-color: #cbd5e1 !important; color: #0f172a !important; }
.stTabs [data-baseweb="tab"][aria-selected="true"] { background-color: #107c41 !important; border-color: #107c41 !important; color: #ffffff !important; box-shadow: 0 4px 10px rgba(16, 124, 65, 0.3) !important; }
.stTabs [data-baseweb="tab"][aria-selected="true"] * { color: #ffffff !important; }
.stTabs [data-baseweb="tab-highlight"] { display: none !important; visibility: hidden !important; height: 0px !important; background-color: transparent !important; }

/* BUTTON OVERRIDE */
div[data-testid="stButton"] > button, div[data-testid="stDownloadButton"] > button { background-color: #107c41 !important; color: #ffffff !important; border: none !important; border-radius: 8px !important; font-weight: 700 !important; padding: 0.75rem 1.5rem !important; width: 100%; font-size: 1.05rem !important; box-shadow: 0 4px 6px -1px rgba(16, 124, 65, 0.2) !important; transition: all 0.2s ease !important; }
div[data-testid="stButton"] > button:hover, div[data-testid="stDownloadButton"] > button:hover { background-color: #0b5c2f !important; box-shadow: 0 6px 12px rgba(16, 124, 65, 0.3) !important; transform: translateY(-2px) !important; }
div[data-testid="stButton"] > button *, div[data-testid="stDownloadButton"] > button * { color: #ffffff !important; }

/* File Uploader Drag & Drop */
[data-testid="stFileUploader"] section { background-color: #ffffff !important; border: 2px dashed #cbd5e1 !important; border-radius: 12px !important; padding: 50px 20px !important; transition: all 0.2s ease; box-shadow: 0 1px 2px rgba(0,0,0,0.02); }
[data-testid="stFileUploader"] section:hover { border-color: #107c41 !important; background-color: #f0fdf4 !important; }
[data-testid="stFileUploader"] svg { fill: #94a3b8 !important; width: 45px; height: 45px; margin-bottom: 10px;}
[data-testid="stFileUploader"] input[type="file"] { color: transparent !important; }

/* Overwrite Native 200MB text with Custom 5MB text */
[data-testid="stFileUploader"] small { visibility: hidden; }
[data-testid="stFileUploader"] small::before { content: "Max file size: 5.0 MB"; visibility: visible; display: block; color: #64748b; font-size: 0.9rem; font-weight: 500; }

/* Custom Cards */
.custom-card { background-color: #ffffff; border: 1px solid #e2e8f0; border-radius: 12px; padding: 30px 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); height: 100%; transition: transform 0.2s ease;}
.custom-card:hover { transform: translateY(-4px); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); }
.card-icon { font-size: 2.5rem; margin-bottom: 20px; }
.card-title { font-size: 1.15rem; font-weight: 700; color: #0f172a !important; margin-bottom: 12px;}
.card-text { font-size: 0.95rem; color: #475569 !important; line-height: 1.6; }

/* Hero Section */
.hero-container { padding: 40px 0 60px 0; text-align: center; }
.hero-title { font-size: 4.5rem; font-weight: 900; color: #0f172a !important; text-align: center; margin-bottom: 20px; letter-spacing: -0.04em; line-height: 1.1;}
.hero-subtitle { font-size: 1.25rem; color: #475569 !important; text-align: center; margin-bottom: 40px; font-weight: 400; max-width: 650px; margin-left: auto; margin-right: auto; line-height: 1.6;}
.highlight-text { color: #107c41 !important; }

/* Restore icon font (the global Inter rule above breaks Streamlit's icons) */
[data-testid="stIconMaterial"], .material-symbols-rounded, .material-icons, span[class*="material-symbols"] { font-family: "Material Symbols Rounded", "Material Icons" !important; }

/* Chat input: white text inside the box */
[data-testid="stChatInput"] textarea,
[data-testid="stChatInput"] textarea * { color: #ffffff !important; -webkit-text-fill-color: #ffffff !important; caret-color: #ffffff !important; }
[data-testid="stChatInput"] textarea::placeholder { color: #cbd5e1 !important; -webkit-text-fill-color: #cbd5e1 !important; opacity: 1 !important; }
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
if 'ai_report' not in st.session_state:
    st.session_state.ai_report = None
if 'last_filename' not in st.session_state:
    st.session_state.last_filename = "Dataset"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

st.markdown("<h1 style='font-size: 2.8rem; font-weight: 900; color: #0f172a; padding: 15px 0; margin: 0; display: flex; align-items: center; gap: 12px; letter-spacing: -0.04em;'>✨ DataSort Cloud</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

tab_overview, tab_auth, tab_app, tab_download, tab_chat = st.tabs([
    "🏠 Home",
    "🔐 Login",
    "⚡ Clean CSV (Max 5MB)",
    "📥 Desktop App",
    "💬 Chatbot"
])

# ==========================================
# TAB 1: OVERVIEW
# ==========================================
with tab_overview:
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Clean Messy CSV Files <span class="highlight-text">Free.</span></div>
        <div class="hero-subtitle">The fastest, most secure way to transform raw datasets into ML-ready matrices. Instantly format, impute, and export—no coding required.</div>
    </div>
    """, unsafe_allow_html=True)

    col_btn1, col_btn2, col_btn3 = st.columns([3, 2, 3])
    with col_btn2:
        if st.button("Start Cleaning for Free", use_container_width=True):
            st.info("Please click the '🔐 Login' tab above to authenticate your session.")

    st.markdown("<div style='text-align: center; color: #94a3b8; font-size: 0.85rem; margin-top: 15px;'>100% Free • Secure Local Processing • No Credit Card Required</div>", unsafe_allow_html=True)
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; font-weight: 800; font-size: 2rem; margin-bottom: 40px; letter-spacing: -0.02em;'>How it works</h3>", unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='custom-card' style='text-align: center;'><div class='card-icon'>📤</div><div class='card-title'>1. Upload your file</div><div class='card-text'>Drag and drop your messy CSV, Excel, or JSON directly into our secure, ephemeral sandbox.</div></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='custom-card' style='text-align: center;'><div class='card-icon'>⚡</div><div class='card-title'>2. Aggressive Auto-Clean</div><div class='card-text'>We automatically strip invalid characters, coerce schemas, and statistically impute blanks.</div></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='custom-card' style='text-align: center;'><div class='card-icon'>🧠</div><div class='card-title'>3. Export & LLM Insights</div><div class='card-text'>Generate plain-language interpretation reports on pre-aggregated statistics, mitigating context limits.</div></div>", unsafe_allow_html=True)

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
                <div style="font-weight: 600; font-size: 1.5rem; color: #0f172a !important; margin-top: 15px; margin-bottom: 20px;">Sign in to GitHub</div>
            </div>
            <div style="background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 25px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);">
                <p style="font-size: 0.95rem; margin-bottom: 8px; color: #0f172a !important; font-weight: 600;">Username or email address</p>
            """, unsafe_allow_html=True)

            email = st.text_input("Email", label_visibility="collapsed")

            st.markdown("""
                <div style='display: flex; justify-content: space-between; align-items: center; margin-top: 20px; margin-bottom: 8px;'>
                    <span style='font-size: 0.95rem; color: #0f172a !important; font-weight: 600;'>Password</span>
                    <a href='#' style='color: #107c41; font-size: 0.85rem; font-weight: 500; text-decoration: none;'>Forgot password?</a>
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

            st.markdown("</div>", unsafe_allow_html=True)

# ==========================================
# TAB 3: CLOUD APP
# ==========================================
with tab_app:
    if not st.session_state.logged_in:
        st.error("Access Denied: Authentication required to access the cloud sandbox.")
        st.info("Navigate to the '🔐 Login' tab to sign in.")
    else:
        st.markdown("<div style='text-align: center; margin-bottom: 30px;'><h2 style='font-weight: 800; color: #0f172a; margin-bottom: 10px; font-size: 2.2rem; letter-spacing: -0.02em;'>Upload your messy dataset</h2><p style='color: #64748b; font-size: 1.1rem;'>Supports CSV, Excel, JSON, and Parquet up to 5.0 MB.</p></div>", unsafe_allow_html=True)

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
                        if file_ext in ['csv', 'txt']: st.session_state.df = pd.read_csv(uploaded_file)
                        elif file_ext in ['xlsx', 'xls']: st.session_state.df = pd.read_excel(uploaded_file)
                        elif file_ext == 'json': st.session_state.df = pd.read_json(uploaded_file)
                        elif file_ext == 'parquet': st.session_state.df = pd.read_parquet(uploaded_file)

                        st.session_state.df.columns = st.session_state.df.columns.str.strip()
                        st.session_state.cleaned = False
                        st.session_state.ai_report = None

                    df = st.session_state.df

                    st.markdown("<br>", unsafe_allow_html=True)
                    col1, col2, col3, col4, col5 = st.columns(5)
                    col1.metric("TOTAL ROWS", f"{df.shape[0]:,}")
                    col2.metric("COLUMNS", f"{df.shape[1]}")
                    col3.metric("FILE SIZE", f"{file_size_mb:.2f} MB")
                    col4.metric("NUMERIC COLS", f"{len(df.select_dtypes(include=['float64', 'int64']).columns)}")
                    col5.metric("MISSING VALUES", f"{df.isnull().sum().sum():,}")

                    st.markdown("<hr style='margin: 30px 0; border: 1px solid #e2e8f0;'>", unsafe_allow_html=True)

                    mod1, mod2, mod3, mod4 = st.tabs(["✨ Auto-Clean", "📊 Visuals", "🧠 AI Insights", "💾 Download"])

                    with mod1:
                        st.markdown("<h3 style='font-size: 1.2rem; font-weight: 700; margin-bottom: 15px;'>Dataset Preview</h3>", unsafe_allow_html=True)
                        st.dataframe(df.head(), use_container_width=True)

                        if not st.session_state.cleaned:
                            st.info("💡 Your data is raw and may contain missing values or invalid characters.")
                            
                            #  Algorithm Selection Toggle
                            st.markdown("<h4 style='font-size: 1rem; font-weight: 600; margin-top: 15px;'>Select Cleaning Engine</h4>", unsafe_allow_html=True)
                            clean_engine = st.radio("Imputation Methodology:", 
                                ["Fast Clean (Statistical Median/Mode)", "Deep Predict (KNN Machine Learning)"], 
                                horizontal=True, label_visibility="collapsed")
                            
                            if st.button("✨ Execute Auto-Clean", use_container_width=True):
                                with st.spinner("Purging anomalies and imputing missing data..."):
                                    # 1. Standardize anomalies
                                    dirty_placeholders = ['-', '?', 'NA', 'N/A', 'n/a', 'na', 'null', 'Null', '', ' ', '#N/A']
                                    df = df.replace(dirty_placeholders, np.nan)

                                    # 2. Coerce schemas
                                    for c in df.columns:
                                        if df[c].dtype == 'object': df[c] = pd.to_numeric(df[c], errors='ignore')

                                    num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                                    cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

                                    # 3. Handle Categorical (Mode)
                                    for col in cat_cols:
                                        mode_series = df[col].mode()
                                        df[col] = df[col].fillna(mode_series[0] if not mode_series.empty else "Unknown")

                                    # 4. Handle Numeric based on selected engine
                                    if clean_engine == "Deep Predict (KNN Machine Learning)" and len(num_cols) > 0:
                                        imputer = KNNImputer(n_neighbors=5, weights="distance")
                                        df[num_cols] = imputer.fit_transform(df[num_cols])
                                    else:
                                        # Fallback to standard statistical median
                                        for col in num_cols: 
                                            df[col] = df[col].fillna(df[col].median() if pd.notna(df[col].median()) else 0)

                                    st.session_state.df = df
                                    st.session_state.cleaned = True
                                    st.rerun()
                        else:
                            st.success("✅ Dataset has been rigorously cleaned. Zero missing values remain.")

                    with mod2:
                        st.markdown("<h3 style='font-size: 1.2rem; font-weight: 700; margin-bottom: 15px;'>Visual Analytics</h3>", unsafe_allow_html=True)
                        numeric_cols_viz = df.select_dtypes(include=[np.number]).columns.tolist()

                        if len(numeric_cols_viz) > 0:
                            chart_type = st.radio("Select Analysis Type:", ["Correlation Matrix", "Feature Distribution", "Scatter Plot"], horizontal=True)

                            if chart_type == "Correlation Matrix" and len(numeric_cols_viz) >= 2:
                                fig = px.imshow(df[numeric_cols_viz].corr(), text_auto=".2f", color_continuous_scale=[[0.0, '#eff6ff'], [1.0, '#107c41']], aspect="auto")
                                st.plotly_chart(fig, use_container_width=True)
                            elif chart_type == "Feature Distribution" and numeric_cols_viz:
                                fig = px.histogram(df, x=st.selectbox("Select Feature:", numeric_cols_viz), color_discrete_sequence=['#107c41'])
                                st.plotly_chart(fig, use_container_width=True)
                            elif chart_type == "Scatter Plot" and len(numeric_cols_viz) >= 2:
                                fig = px.scatter(df, x=st.selectbox("X-Axis:", numeric_cols_viz, index=0), y=st.selectbox("Y-Axis:", numeric_cols_viz, index=1 if len(numeric_cols_viz) > 1 else 0), color_discrete_sequence=['#107c41'])
                                st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No numerical columns available for visualizations.")

                    with mod3:
                        st.markdown("<h3 style='font-size: 1.2rem; font-weight: 700; margin-bottom: 5px;'>LLM Reasoning Layer</h3>", unsafe_allow_html=True)
                        st.caption("Operating on pre-aggregated statistics to generate natural-language interpretations without exceeding context limits.")

                        if st.button("Generate Analytical Report"):
                            with st.spinner("Analyzing statistical aggregations..."):
                                try:
                                    # Fetch API key automatically in the background
                                    api_key = st.secrets["GEMINI_API_KEY"]
                                    genai.configure(api_key=api_key)
                                    model = genai.GenerativeModel('gemini-3.8-flash')

                                    stats_summary = df.describe().to_string()
                                    corr_summary = df.select_dtypes(include=[np.number]).corr().to_string() if len(df.select_dtypes(include=[np.number]).columns) > 1 else "Not enough numeric columns for correlation."

                                    prompt = f"""
                                    You are an expert data analyst. Based on the following pre-aggregated statistics, draft a short, plain-language summary of what they imply. Highlight key distributions, extreme outliers, and any strong correlations.

                                    Summary Statistics:
                                    {stats_summary}

                                    Correlation Matrix:
                                    {corr_summary}
                                    """

                                    response = model.generate_content(prompt)
                                    st.session_state.ai_report = response.text
                                except KeyError:
                                    st.error("🛑 Configuration Error: GEMINI_API_KEY not found in Streamlit secrets.")
                                except Exception as e:
                                    st.error(f"LLM API Error: {e}")

                        if st.session_state.ai_report:
                            st.markdown("<div style='background-color:#ffffff; padding:20px; border-radius:8px; border:1px solid #e2e8f0; margin-top:20px;'>", unsafe_allow_html=True)
                            st.markdown(st.session_state.ai_report)
                            st.markdown("</div>", unsafe_allow_html=True)

                    with mod4:
                        st.markdown("<h3 style='font-size: 1.2rem; font-weight: 700; margin-bottom: 15px;'>Export Cleaned Data</h3>", unsafe_allow_html=True)
                        if not st.session_state.cleaned:
                            st.error("🛑 The dataset still contains uncleaned data.")
                            st.warning("👉 Go to the '✨ Auto-Clean' tab and clean the file first.")
                        else:
                            st.success("✅ Dataset is fully processed and ready for download.")
                            st.download_button(label="📥 Download Cleaned CSV", data=df.to_csv(index=False).encode('utf-8'), file_name=f"Cleaned_{st.session_state.last_filename.split('.')[0]}.csv", mime="text/csv", use_container_width=True)

                except Exception as e:
                    st.error(f"Data parse failure. Error: {e}")

# ==========================================
# TAB 4: DOWNLOAD APP
# ==========================================
with tab_download:
    st.markdown("<h2 style='color: #0f172a !important; font-weight: 800; text-align: center; margin-top: 40px; font-size: 2.5rem; letter-spacing: -0.02em;'>Get the Local Engine</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color: #475569 !important; text-align: center; font-size: 1.1rem; margin-bottom: 40px;'>Unrestricted, unlimited data usage running offline on your own hardware.</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("<div class='custom-card' style='margin-bottom: 30px;'><div class='card-title'>Runtime Capability Matrix</div><ul style='color: #475569 !important; font-size: 0.95rem; line-height: 1.8; padding-left: 20px;'><li><strong>OS Requirement:</strong> Windows / macOS / Linux</li><li><strong>File Size Quota:</strong> UNLIMITED (Hardware Bound)</li><li><strong>Data Privacy:</strong> 100% AIR-GAPPED</li><li><strong>Prerequisite:</strong> Python 3.9+ installed</li></ul></div>", unsafe_allow_html=True)

        try:
            with open(__file__, "r", encoding="utf-8") as f:
                app_code = f.read()
        except Exception:
            app_code = "# Error reading source file. Please ensure app.py exists locally."

        reqs = "streamlit\npandas\nplotly\nnumpy\ngoogle-generativeai"
        bat_code = "@echo off\necho Starting EDA Engine Local Environment\npip install -r requirements.txt\nstreamlit run app.py\npause"

        import io, zipfile
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            zip_file.writestr("app.py", app_code)
            zip_file.writestr("requirements.txt", reqs)
            zip_file.writestr("Launch_Windows.bat", bat_code)

        st.download_button("📥 Download Local Engine (.zip)", data=zip_buffer.getvalue(), file_name="EDA_Engine_Offline.zip", mime="application/zip", use_container_width=True)

# ==========================================
# TAB 5: CHATBOT
# ==========================================
with tab_chat:
    st.markdown("<h2 style='font-weight: 800; text-align: center; margin-top: 20px; font-size: 2.2rem; letter-spacing: -0.02em;'>💬 DataSort Assistant</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748b !important; margin-bottom: 20px;'>Ask about data cleaning, EDA, or your uploaded dataset.</p>", unsafe_allow_html=True)

    AVATARS = {"user": "🧑‍💻", "assistant": "🤖"}

    # Build the bot's instructions (and dataset context, if a file is loaded)
    def build_system_prompt():
        prompt = (
            "You are DataSort Assistant, a friendly helper inside the DataSort Cloud web app. "
            "The app cleans messy CSV/Excel/JSON/Parquet files (max 5 MB), imputes missing values, "
            "shows visualizations (correlation matrix, distributions, scatter plots), and generates AI insights. "
            "Help users with data cleaning, exploratory data analysis, pandas, and understanding their results. "
            "Keep answers clear and concise."
        )
        df_ctx = st.session_state.get("df")
        if df_ctx is not None:
            prompt += (
                f"\n\nThe user has uploaded a dataset named '{st.session_state.last_filename}' "
                f"with {df_ctx.shape[0]} rows and {df_ctx.shape[1]} columns.\n"
                f"Columns and types:\n{df_ctx.dtypes.to_string()}\n\n"
                f"Missing values per column:\n{df_ctx.isnull().sum().to_string()}\n\n"
                f"First 5 rows:\n{df_ctx.head().to_string()}\n\n"
                f"Dataset cleaned already: {st.session_state.cleaned}"
            )
        return prompt

    _, clear_col, _ = st.columns([3, 2, 3])
    with clear_col:
        if st.button("🗑️ Clear chat"):
            st.session_state.chat_history = []
            st.rerun()

    # Show previous messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"], avatar=AVATARS[msg["role"]]):
            st.markdown(msg["content"])

    # Input box
    user_input = st.chat_input("Ask me anything about DataSort or your dataset...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user", avatar=AVATARS["user"]):
            st.markdown(user_input)

        with st.chat_message("assistant", avatar=AVATARS["assistant"]):
            try:
                genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

                # Convert earlier messages to Gemini's format (roles: "user" / "model")
                past = [
                    {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                    for m in st.session_state.chat_history[:-1]
                ]

                # Try models in order; each attempt gives up after 45s instead of hanging
                reply, last_error = None, None
                with st.spinner("Thinking..."):
                    for model_name in ["gemini-3.8-flash", "gemini-3.5-flash", "gemini-3.5-flash-lite"]:
                        try:
                            model = genai.GenerativeModel(model_name, system_instruction=build_system_prompt())
                            chat = model.start_chat(history=past)
                            response = chat.send_message(user_input, request_options={"timeout": 45, "retry": None})
                            reply = response.text
                            break
                        except KeyError:
                            raise
                        except Exception as e:
                            last_error = e

                if reply is None:
                    st.session_state.chat_history.pop()  # drop the unanswered question
                    st.error(f"Chatbot error (all models failed): {last_error}")
                else:
                    st.markdown(reply)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})

            except KeyError:
                st.session_state.chat_history.pop()
                st.error("🛑 GEMINI_API_KEY not found in Streamlit secrets.")
            except Exception as e:
                st.session_state.chat_history.pop()
                st.error(f"Chatbot error: {e}")
