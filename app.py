import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 1. Page Configuration & Professional Theming
st.set_page_config(page_title="AI EDA Generator | Launch", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    html, body, [class*="css"]  { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .main-title { font-size: 3rem; color: #0F172A; font-weight: 800; text-align: center; margin-bottom: 0px; padding-top: 10px;}
    .sub-title { font-size: 1.2rem; color: #64748B; text-align: center; margin-bottom: 40px; font-weight: 400; }
    .feature-box { background-color: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 10px; padding: 20px; margin-bottom: 20px;}
</style>
""", unsafe_allow_html=True)

# 2. Session State Management
if 'df' not in st.session_state:
    st.session_state.df = None
if 'cleaned' not in st.session_state:
    st.session_state.cleaned = False
if 'last_file' not in st.session_state:
    st.session_state.last_file = ""

# 3. Global Site Navigation (The Freemium Funnel)
with st.sidebar:
    st.markdown("<h2 style='text-align: center;'>🌐 Site Navigation</h2>", unsafe_allow_html=True)
    site_mode = st.radio("Choose Mode:", ["🏠 Product Launch Page", "⚡ Try Lite Web Version"], label_visibility="collapsed")
    st.markdown("---")
    st.markdown("### 🎓 Project Details")
    st.markdown("**Platform:** AI EDA Generator")
    st.markdown("**Institution:** Inderprastha Engineering College (IPEC)")
    st.markdown("**Dept:** CSE (Data Science) - Group 16")
    st.markdown("**Guidance:** Bhanu Bhardwaj")

# ==========================================
# MODE 1: THE PRODUCT LAUNCH PAGE
# ==========================================
if site_mode == "🏠 Product Launch Page":
    st.markdown('<p class="main-title">📈 AI EDA Generator</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">The Ultimate Offline Exploratory Data Analysis Pipeline</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.info("🚀 **Version 1.0 is Live!** Transform raw, dirty data into ML-ready datasets in one click. Built for data privacy, offline environments, and high-performance computing.")
        
        # Fake .exe file generation for presentation demo purposes
        dummy_exe_bytes = b"This is a placeholder for the compiled AI_EDA_Generator.exe file."
        
        st.markdown("### 📥 Download the Full Windows App")
        st.write("Get the unrestricted, 100% offline desktop application. Includes the NLP Data Chatbot, IEEE Report Generator, and massive file support (1GB+).")
        st.download_button(
            label="🖥️ Download for Windows (.exe)", 
            data=dummy_exe_bytes, 
            file_name="AI_EDA_Generator_Setup.exe", 
            mime="application/octet-stream",
            use_container_width=True
        )
        
        st.markdown("<br><hr><br>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Don't want to download yet?</h3>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Use the sidebar to navigate to the <b>Lite Web Version</b> to test basic profiling and visualization (Limited to 5MB files).</p>", unsafe_allow_html=True)

# ==========================================
# MODE 2: THE LITE WEB VERSION
# ==========================================
elif site_mode == "⚡ Try Lite Web Version":
    
    st.markdown('<p class="main-title">⚡ AI EDA Generator (Lite)</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Web Version - Limited Features & 5MB File Cap</p>', unsafe_allow_html=True)
    
    # Lite Version File Ingestion
    with st.sidebar:
        st.header("📂 Data Ingestion")
        uploaded_file = st.file_uploader("Upload Dataset (Any File Format)")
        
        if uploaded_file:
            file_size_mb = uploaded_file.size / (1024 * 1024)
            
            # THE FREEMIUM LIMITER
            if file_size_mb > 5.0:
                st.error(f"🛑 File too large ({file_size_mb:.1f}MB). The web version is capped at 5MB to save server resources.")
                st.warning("👉 Return to the 'Product Launch Page' to download the unlimited Windows app.")
            else:
                try:
                    if st.session_state.df is None or st.session_state.last_file != uploaded_file.name:
                        file_ext = uploaded_file.name.split('.')[-1].lower()
                        success = False
                        
                        if file_ext in ['csv', 'txt']:
                            df_raw = pd.read_csv(uploaded_file, low_memory=False)
                            success = True
                        elif file_ext in ['xlsx', 'xls']:
                            df_raw = pd.read_excel(uploaded_file)
                            success = True
                        elif file_ext == 'json':
                            df_raw = pd.read_json(uploaded_file)
                            success = True
                        elif file_ext == 'parquet':
                            df_raw = pd.read_parquet(uploaded_file)
                            success = True
                        elif file_ext in ['docx', 'doc', 'pdf']:
                            st.error(f"⚠️ Text documents cannot be mathematically analyzed.")
                        elif file_ext == 'pbix':
                            st.error("⚠️ Power BI files are dashboards, not raw datasets. Export to CSV first.")
                        else:
                            st.error(f"⚠️ Unsupported format: .{file_ext}.")
                        
                        if success:
                            st.session_state.df = df_raw
                            st.session_state.df.columns = st.session_state.df.columns.str.strip()
                            st.session_state.last_file = uploaded_file.name
                            st.session_state.cleaned = False
                            st.toast(f'Dataset loaded!', icon='✅')
                
                except Exception as e:
                    st.error(f"Error details: {e}")

        st.markdown("---")
        st.header("🧭 Lite Menu")
        # PREMIUM FEATURES REMOVED FROM RADIO BUTTON
        selected_view = st.radio("Navigation", [
            "🗄️ Profiling & Cleaning", 
            "📉 Visual Analytics",
            "🔒 Advanced Features (Locked)"
        ], label_visibility="collapsed")

    # Lite Version App Layout
    if st.session_state.df is not None:
        df = st.session_state.df
        
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Observations", f"{df.shape[0]:,}")
        m2.metric("Feature Count", df.shape[1])
        m3.metric("Missing Values", df.isnull().sum().sum())
        m4.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        st.markdown("<hr>", unsafe_allow_html=True)
        
        if selected_view == "🗄️ Profiling & Cleaning":
            col1, col2 = st.columns([1, 2])
            with col1:
                missing_data = pd.DataFrame({'Data Type': df.dtypes, 'Missing': df.isnull().sum()})
                st.dataframe(missing_data, use_container_width=True, height=300)
                
                if not st.session_state.cleaned:
                    if st.button("✨ Execute Auto-Clean", use_container_width=True):
                        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
                        for col in num_cols:
                            df[col] = df[col].fillna(df[col].median() if pd.notna(df[col].median()) else 0)
                        st.session_state.df = df
                        st.session_state.cleaned = True
                        st.rerun()
                else:
                    st.success("✅ Dataset cleaned.")
            with col2:
                st.dataframe(df.describe().T, use_container_width=True, height=300)
                
        elif selected_view == "📉 Visual Analytics":
            numeric_cols_viz = df.select_dtypes(include=[np.number]).columns.tolist()
            chart_type = st.radio("Select:", ["Correlation", "Distribution"], horizontal=True)
            
            if chart_type == "Correlation" and len(numeric_cols_viz) >= 2:
                fig = px.imshow(df[numeric_cols_viz].corr(), text_auto=".2f", color_continuous_scale=[[0.0, '#2563EB'], [1.0, '#10B981']], aspect="auto")
                st.plotly_chart(fig, use_container_width=True)
            elif chart_type == "Distribution" and numeric_cols_viz:
                selected_col = st.selectbox("Feature:", numeric_cols_viz)
                fig = px.histogram(df, x=selected_col, color_discrete_sequence=['#3B82F6'])
                st.plotly_chart(fig, use_container_width=True)

        elif selected_view == "🔒 Advanced Features (Locked)":
            st.error("🔒 **Premium Features Locked**")
            st.write("The **AI NLP Chatbot Engine**, **IEEE Report Generator**, and **Massive Data Export** are only available in the full offline desktop application.")
            st.write("👉 Go back to the **Product Launch Page** to download the unrestricted Windows version.")

    else:
        st.info("👈 Upload a dataset (Under 5MB) via the sidebar to test the Lite version.")
