import streamlit as st
import pandas as pd

# 1. Page Configuration & Modern SaaS UI
st.set_page_config(page_title="AI EDA Generator | Launch", page_icon="🚀", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    html, body, [class*="css"]  { font-family: 'Inter', sans-serif; }
    
    .hero-title { font-size: 3.5rem; color: #0F172A; font-weight: 900; text-align: center; margin-bottom: 0px; padding-top: 40px; line-height: 1.2;}
    .hero-subtitle { font-size: 1.2rem; color: #475569; text-align: center; margin-bottom: 40px; margin-top: 20px; font-weight: 400; max-width: 800px; margin-left: auto; margin-right: auto;}
    
    .feature-card { background-color: #ffffff; border: 1px solid #E2E8F0; border-radius: 12px; padding: 25px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); text-align: center; height: 100%;}
    .feature-icon { font-size: 2.5rem; margin-bottom: 15px; }
    .feature-title { font-size: 1.2rem; font-weight: 700; color: #1E293B; margin-bottom: 10px;}
    
    .lock-box { background-color: #FFFBEB; border: 1px solid #FDE68A; border-radius: 10px; padding: 20px; text-align: center; margin-top: 20px;}
</style>
""", unsafe_allow_html=True)

# 2. Session State for Authentication
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# 3. App Navigation
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🌐 Platform Menu</h2>", unsafe_allow_html=True)
    
    if st.session_state.logged_in:
        st.success(f"👋 Welcome, {st.session_state.username}!")
        if st.button("Log Out", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
            
    nav = st.radio("Navigate", ["🏠 Home", "🔐 Sign In / Register", "⚡ Try Web App (Lite)", "📥 Download Full App (Offline)"], label_visibility="collapsed")
    st.markdown("---")
    st.caption("© 2026 AI EDA Generator | IPEC Group 16")

# ==========================================
# PAGE 1: MODERN LANDING PAGE (Like cleanmyexcel.io)
# ==========================================
if nav == "🏠 Home":
    st.markdown('<p class="hero-title">Stop Wasting Hours on Dirty Data.</p>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">The ultimate AI-powered Exploratory Data Analysis tool. Auto-clean matrices, generate IEEE reports, and chat with your datasets instantly.</p>', unsafe_allow_html=True)
    
    col_btn1, col_btn2, col_btn3 = st.columns([1.5, 1, 1.5])
    with col_btn2:
        if st.button("🚀 Get Started for Free", use_container_width=True, type="primary"):
            st.info("👈 Please use the sidebar to Sign In or Try the Web App.")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Feature Cards
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔒</div>
            <div class="feature-title">100% Offline & Secure</div>
            <p style="color: #64748B; font-size: 0.95rem;">Our desktop app runs natively on your machine. Zero data is sent to the cloud, ensuring total compliance for healthcare and finance.</p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">⚡</div>
            <div class="feature-title">Aggressive Auto-Clean</div>
            <p style="color: #64748B; font-size: 0.95rem;">One click purges garbage text, drops nulls, and mathematically imputes missing values using median/mode optimization.</p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🤖</div>
            <div class="feature-title">NLP Data Assistant</div>
            <p style="color: #64748B; font-size: 0.95rem;">Chat directly with your dataset. Ask for correlations, maximums, or statistics in plain English, completely offline.</p>
        </div>
        """, unsafe_allow_html=True)

# ==========================================
# PAGE 2: AUTHENTICATION SYSTEM
# ==========================================
elif nav == "🔐 Sign In / Register":
    st.markdown("<h2 style='text-align: center;'>Access Your Account</h2>", unsafe_allow_html=True)
    
    if st.session_state.logged_in:
        st.success("You are already logged in! Proceed to 'Try Web App' or 'Download Full App'.")
    else:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            tab1, tab2 = st.tabs(["Sign In", "Create Account"])
            
            with tab1:
                st.text_input("Email Address")
                st.text_input("Password", type="password")
                if st.button("Secure Login", use_container_width=True, type="primary"):
                    st.session_state.logged_in = True
                    st.session_state.username = "DataScientist_01"
                    st.success("Authentication successful! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                    
            with tab2:
                st.text_input("Full Name")
                st.text_input("Corporate Email")
                st.text_input("Choose Password", type="password")
                if st.button("Create Free Account", use_container_width=True):
                    st.session_state.logged_in = True
                    st.session_state.username = "New_User"
                    st.balloons()
                    st.success("Account Created! Welcome aboard.")
                    time.sleep(1.5)
                    st.rerun()

# ==========================================
# PAGE 3: LITE WEB APP (The Teaser Funnel)
# ==========================================
elif nav == "⚡ Try Web App (Lite)":
    if not st.session_state.logged_in:
        st.warning("⚠️ You must Sign In to use the web application.")
        st.info("👈 Use the sidebar menu to Create an Account or Log In.")
    else:
        st.markdown("### ⚡ AI EDA Generator - Cloud Teaser")
        st.write("Upload a small file to preview how the engine parses structural data.")
        
        uploaded_file = st.file_uploader("Upload File (Strict 5MB Limit)", type=['csv', 'xlsx', 'json'])
        
        if uploaded_file:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            
            if file_size_mb > 5.0:
                st.error(f"🛑 SERVER REJECTED: Your file is {file_size_mb:.2f}MB. Free cloud accounts are restricted to 5MB to prevent server overload.")
                st.markdown("[📥 Download the Desktop App for Unlimited Data](#)")
            else:
                try:
                    df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
                    st.success("File ingested successfully!")
                    
                    st.markdown("#### 🔍 Data Preview (First 5 Rows)")
                    st.dataframe(df.head())
                    
                    st.markdown("#### 📊 Structural Architecture")
                    col1, col2 = st.columns(2)
                    col1.metric("Rows", df.shape[0])
                    col2.metric("Columns", df.shape[1])
                    
                    # UPSELL / PREMIUM LOCK
                    st.markdown("""
                    <div class="lock-box">
                        <h3 style="color: #B45309; margin-top:0;">🔒 Premium Features Locked</h3>
                        <p style="color: #92400E; font-size: 14px;">The <b>Aggressive Cleaning Engine</b>, <b>Visual Analytics Suite</b>, and <b>NLP Chatbot</b> are disabled in the web preview.</p>
                        <p style="color: #92400E; font-size: 14px;">To unlock enterprise-grade processing and massive file support, please download the local Windows application.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
                except Exception as e:
                    st.error("Failed to parse file.")

# ==========================================
# PAGE 4: DOWNLOAD APP (The Conversion)
# ==========================================
elif nav == "📥 Download Full App (Offline)":
    st.markdown("<h2 style='text-align: center;'>Download AI EDA Generator</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #64748B;'>Get the full power of offline data science directly on your machine.</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        **What you get in the Desktop Version:**
        * ✅ Unlimited File Size (1GB+ Support via Chunking)
        * ✅ NLP Chatbot & Insight Engine
        * ✅ Automated Math Imputation (Median/Mode)
        * ✅ IEEE Report Generation
        * ✅ Zero Internet Required
        """)
        
        dummy_exe_bytes = b"Placeholder for compiled AI_EDA_Generator.exe"
        st.download_button(
            label="🖥️ Download Windows Installer (.exe)", 
            data=dummy_exe_bytes, 
            file_name="AI_EDA_Generator_Setup.exe", 
            mime="application/octet-stream",
            use_container_width=True,
            type="primary"
        )
