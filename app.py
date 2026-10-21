import streamlit as st
import pandas as pd
import time

# 1. Page Configuration (Minimalist)
st.set_page_config(page_title="EDA Generator", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Clean, modern typography fallback stack */
    html, body, [class*="css"] { 
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; 
    }
    
    /* Stark, monochromatic hero section */
    .hero-title { 
        font-size: 2.8rem; 
        color: #111111; 
        font-weight: 600; 
        text-align: center; 
        margin-top: 60px; 
        margin-bottom: 15px; 
        letter-spacing: -0.02em; 
    }
    .hero-subtitle { 
        font-size: 1.1rem; 
        color: #666666; 
        text-align: center; 
        margin-bottom: 50px; 
        font-weight: 400; 
        max-width: 600px; 
        margin-left: auto; 
        margin-right: auto; 
        line-height: 1.6;
    }
    
    /* Flat, border-only cards with no heavy shadows */
    .card { 
        border: 1px solid #EAEAEA; 
        padding: 24px; 
        border-radius: 4px; 
        height: 100%; 
        background-color: #FFFFFF;
    }
    .card-title { 
        font-size: 1.05rem; 
        font-weight: 600; 
        color: #111111; 
        margin-bottom: 8px; 
    }
    .card-text { 
        font-size: 0.9rem; 
        color: #666666; 
        line-height: 1.6; 
    }
    
    /* Subtle notification boxes instead of loud colored alerts */
    .notice-box { 
        border: 1px solid #EAEAEA; 
        background-color: #FAFAFA; 
        padding: 16px 20px; 
        border-radius: 4px; 
        margin-top: 20px; 
    }
    .notice-title { font-weight: 600; color: #111111; font-size: 0.95rem; margin-bottom: 4px; }
    .notice-text { color: #666666; font-size: 0.9rem; }
    
    /* Minimalist dividers */
    hr { margin-top: 30px; margin-bottom: 30px; border-color: #F3F4F6; }
</style>
""", unsafe_allow_html=True)

# 2. Session State for Authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# 3. Clean Sidebar Navigation
with st.sidebar:
    st.markdown("<h3 style='color: #111; font-weight: 600; font-size: 1.1rem;'>Menu</h3>", unsafe_allow_html=True)
    
    if st.session_state.logged_in:
        st.markdown(f"<p style='color: #666; font-size: 0.9rem;'>Logged in as {st.session_state.username}</p>", unsafe_allow_html=True)
        if st.button("Sign Out", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
            
    nav = st.radio("Navigate", ["Overview", "Authentication", "Web Preview", "Download Software"], label_visibility="collapsed")
    st.markdown("<br><br><p style='color: #999; font-size: 0.8rem;'>v1.0.0 &copy; 2026</p>", unsafe_allow_html=True)

# ==========================================
# PAGE 1: OVERVIEW (Minimal Landing Page)
# ==========================================
if nav == "Overview":
    st.markdown('<p class="hero-title">Automated Data Preprocessing.</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">A high-performance pipeline designed to ingest, clean, and profile raw data environments with absolute privacy.</p>', unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1.5, 1, 1.5])
    with col_btn2:
        if st.button("Get Started", use_container_width=True, type="primary"):
            st.info("Navigate to 'Authentication' in the sidebar to begin.")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="card">
            <div class="card-title">Local Execution</div>
            <div class="card-text">Engineered to run natively on local hardware. Zero data is transmitted externally, ensuring strict compliance with data privacy regulations.</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="card">
            <div class="card-title">Vectorized Cleaning</div>
            <div class="card-text">Bypasses manual scripting by automatically purging anomalies, coercing types, and applying statistical imputation to missing matrices.</div>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="card">
            <div class="card-title">NLP Integration</div>
            <div class="card-text">Query datasets using standard natural language. The deterministic engine processes instructions and outputs quantitative results instantly.</div>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# PAGE 2: AUTHENTICATION
# ==========================================
elif nav == "Authentication":
    st.markdown("<h3 style='color: #111; font-weight: 600; text-align: center; margin-bottom: 20px;'>Account Access</h3>", unsafe_allow_html=True)
    
    if st.session_state.logged_in:
        st.success("Session active. You may proceed to the Web Preview or Download sections.")
    else:
        col1, col2, col3 = st.columns([1, 1.5, 1])
        with col2:
            tab1, tab2 = st.tabs(["Sign In", "Register"])
            
            with tab1:
                st.text_input("Email")
                st.text_input("Password", type="password")
                if st.button("Authenticate", use_container_width=True):
                    st.session_state.logged_in = True
                    st.session_state.username = "Analyst_01"
                    st.success("Authenticated.")
                    time.sleep(0.5)
                    st.rerun()
                    
            with tab2:
                st.text_input("Organization")
                st.text_input("Work Email")
                st.text_input("Create Password", type="password")
                if st.button("Create Account", use_container_width=True):
                    st.session_state.logged_in = True
                    st.session_state.username = "New_Analyst"
                    st.success("Account provisioned.")
                    time.sleep(0.5)
                    st.rerun()

# ==========================================
# PAGE 3: WEB PREVIEW (The Limit Funnel)
# ==========================================
elif nav == "Web Preview":
    if not st.session_state.logged_in:
        st.warning("Authentication required to access the data preview environment.")
    else:
        st.markdown("<h3 style='color: #111; font-weight: 600;'>Cloud Preview Environment</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color: #666; font-size: 0.95rem; margin-bottom: 20px;'>Upload a sample file to view structural profiling. Note: Cloud processing is capped at 5MB.</p>", unsafe_allow_html=True)
        
        uploaded_file = st.file_uploader("Select File", type=['csv', 'xlsx', 'json'], label_visibility="collapsed")
        
        if uploaded_file:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            
            if file_size_mb > 5.0:
                st.error(f"Execution Halted: File exceeds 5.0MB payload limit ({file_size_mb:.2f}MB detected).")
                st.markdown("Navigate to 'Download Software' for unrestricted local processing.")
            else:
                try:
                    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                    
                    st.markdown("<hr>", unsafe_allow_html=True)
                    st.markdown("<h4 style='color: #111; font-weight: 600; font-size: 1rem;'>Matrix Structure</h4>", unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                    col1.metric("Observations (Rows)", df.shape[0])
                    col2.metric("Features (Columns)", df.shape[1])
                    
                    st.markdown("<br><h4 style='color: #111; font-weight: 600; font-size: 1rem;'>Data Preview</h4>", unsafe_allow_html=True)
                    st.dataframe(df.head())
                    
                    st.markdown("""
                    <div class="notice-box">
                        <div class="notice-title">Action Required: Download for Full Functionality</div>
                        <div class="notice-text">Mathematical imputation, visual rendering, and NLP querying are restricted in the web preview to preserve server bandwidth. Download the desktop executable for the complete preprocessing pipeline.</div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error("Data parse failure. Ensure file format is valid.")

# ==========================================
# PAGE 4: DOWNLOAD APP
# ==========================================
elif nav == "Download Software":
    st.markdown("<h3 style='color: #111; font-weight: 600; text-align: center;'>Local Deployment</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #666; text-align: center; font-size: 0.95rem; margin-bottom: 40px;'>Acquire the standalone Windows executable for unrestricted, offline usage.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div class="card" style="background-color: #FAFAFA;">
            <div class="card-title">System Requirements & Capabilities</div>
            <ul style="color: #666; font-size: 0.9rem; line-height: 1.8;">
                <li>OS: Windows 10/11 (64-bit)</li>
                <li>Processing limit: Unrestricted (Hardware bound)</li>
                <li>Dependencies: None (Packaged runtime)</li>
                <li>Network: 100% Offline execution</li>
            </ul>
        </div>
        <br>
        """, unsafe_allow_html=True)
        
        dummy_exe_bytes = b"Executable build payload"
        st.download_button(
            label="Download Application (Windows x64)", 
            data=dummy_exe_bytes, 
            file_name="EDA_Pipeline_Installer.exe", 
            mime="application/octet-stream",
            use_container_width=True,
            type="primary"
        )
