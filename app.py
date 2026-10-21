import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import time

# 1. Page Configuration & Professional Theming
st.set_page_config(page_title="AI EDA Generator", page_icon="📈", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    html, body, [class*="css"]  { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
    .main-title { font-size: 2.5rem; color: #0F172A; font-weight: 800; text-align: center; margin-bottom: 0px; padding-top: 20px;}
    .sub-title { font-size: 1.1rem; color: #64748B; text-align: center; margin-bottom: 30px; font-weight: 400; }
    div[data-testid="metric-container"] { background-color: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05); transition: transform 0.2s ease;}
    div[data-testid="metric-container"]:hover { transform: translateY(-2px); }
</style>
""", unsafe_allow_html=True)

# 2. Session State Management
if 'df' not in st.session_state:
    st.session_state.df = None
if 'cleaned' not in st.session_state:
    st.session_state.cleaned = False
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'last_file' not in st.session_state:
    st.session_state.last_file = ""

# 3. Sidebar Navigation & Ingestion (Universal Converter)
with st.sidebar:
    st.markdown("<h1 style='text-align: center; margin-bottom: 0;'>⚡</h1>", unsafe_allow_html=True)
    st.header("📂 Data Ingestion")
    
    # Unrestricted Uploader: Accepts any file format
    uploaded_file = st.file_uploader("Upload Dataset (Any File Format)")
    
    if uploaded_file:
        file_size_mb = uploaded_file.size / (1024 * 1024)
        
        # Freemium Web Limit Demo (5MB cap)
        if file_size_mb > 5.0:
            st.error(f"🛑 Web Version Limit: Your file is {file_size_mb:.1f}MB. The free online version is limited to 5MB.")
            st.markdown("[📥 Click here to download the Unlimited Offline Desktop App (.exe)](#)")
        else:
            try:
                if st.session_state.df is None or st.session_state.last_file != uploaded_file.name:
                    
                    file_ext = uploaded_file.name.split('.')[-1].lower()
                    success = False
                    
                    # Convert standard tabular formats
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
                    
                    # Catch proprietary/non-tabular formats gracefully
                    elif file_ext in ['docx', 'doc', 'pdf']:
                        st.error(f"⚠️ We received your '{file_ext.upper()}' document. However, Exploratory Data Analysis requires structured tabular data (rows & columns). Text documents cannot be mathematically analyzed.")
                    elif file_ext == 'pbix':
                        st.error("⚠️ Power BI (.pbix) files are encrypted dashboards, not raw datasets. Please open this file in Power BI, click 'Export Data', and upload the resulting CSV here.")
                    else:
                        st.error(f"⚠️ Unsupported format: .{file_ext}. Please provide a standard data file (CSV, Excel, JSON).")
                    
                    # Only proceed if data conversion was mathematically possible
                    if success:
                        st.session_state.df = df_raw
                        st.session_state.df.columns = st.session_state.df.columns.str.strip()
                        st.session_state.last_file = uploaded_file.name
                        st.session_state.cleaned = False
                        st.session_state.chat_history = [] 
                        st.toast(f'{file_ext.upper()} successfully converted to usable dataset!', icon='✅')
            
            except Exception as e:
                st.error(f"System caught a corrupted or unreadable file. Error details: {e}")

    st.markdown("---")
    st.header("🧭 Main Menu")
    
    selected_view = st.radio("Navigation", [
        "🗄️ Profiling & Cleaning", 
        "📉 Visual Analytics", 
        "🤖 AI Insight & Chat", 
        "📄 IEEE Report Export", 
        "💾 Export Clean Data"
    ], label_visibility="collapsed")
    
    st.markdown("---")
    st.markdown("### 🎓 Project Details")
    st.markdown("**Platform:** AI EDA Generator")
    st.markdown("**Institution:** Inderprastha Engineering College (IPEC)")
    st.markdown("**Dept:** CSE (Data Science) - Group 16")
    st.markdown("**Guidance:** Bhanu Bhardwaj")

# 4. Main Application Layout
st.markdown('<p class="main-title">📈 AI EDA Generator</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Automated Exploratory Data Analysis & Intelligent Insights Platform</p>', unsafe_allow_html=True)

if st.session_state.df is not None:
    df = st.session_state.df
    
    # KPI Dashboard
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Observations", f"{df.shape[0]:,}")
    m2.metric("Feature Count", df.shape[1])
    m3.metric("Missing Values", df.isnull().sum().sum(), delta="- Clean Data Below" if df.isnull().sum().sum() > 0 else "Clean", delta_color="inverse")
    m4.metric("Memory Usage", f"{df.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # --- VIEW 1: PROFILING & CLEANING ---
    if selected_view == "🗄️ Profiling & Cleaning":
        st.markdown("### Dataset Architecture & Aggressive Cleaning")
        col1, col2 = st.columns([1, 2])
        with col1:
            st.markdown("**Data Types & Missing Values**")
            missing_data = pd.DataFrame({'Data Type': df.dtypes, 'Missing': df.isnull().sum()})
            st.dataframe(missing_data, use_container_width=True, height=300)
            
            if not st.session_state.cleaned:
                st.warning("Data is raw. It contains hidden nulls or missing values.")
                if st.button("✨ Execute Aggressive Auto-Clean", use_container_width=True):
                    with st.spinner("Executing high-speed vectorized cleaning..."):
                        obj_cols = df.select_dtypes(include=['object', 'string']).columns
                        if len(obj_cols) > 0:
                            df[obj_cols] = df[obj_cols].replace(r'^\s*$', np.nan, regex=True)
                            garbage_list = ['?', 'NA', 'n/a', 'null', 'Null', '-', 'None', 'NaN', 'nan', '']
                            df[obj_cols] = df[obj_cols].replace(garbage_list, np.nan)
                            
                        df = df.dropna(how='all') 
                        df = df.dropna(axis=1, how='all')
                        
                        for col in obj_cols:
                            try:
                                df[col] = pd.to_numeric(df[col])
                            except Exception:
                                pass
                                    
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
                
        with col2:
            st.markdown("**Statistical Distribution Summary**")
            st.dataframe(df.describe().T, use_container_width=True, height=300)
            
    # --- VIEW 2: VISUAL ANALYTICS ---
    elif selected_view == "📉 Visual Analytics":
        st.markdown("### Automated Visualization Suite")
        
        max_points = 10000
        if len(df) > max_points:
            st.info(f"⚡ High-Performance Mode: Visualizations are sampled to {max_points:,} points to prevent browser lag.")
            plot_df = df.sample(max_points, random_state=42)
        else:
            plot_df = df
            
        numeric_cols_viz = plot_df.select_dtypes(include=[np.number]).columns.tolist()
        
        chart_type = st.radio("Select Analysis Type:", ["Correlation Analysis", "Feature Distribution", "Bivariate Scatter"], horizontal=True)
        if chart_type == "Correlation Analysis" and len(numeric_cols_viz) >= 2:
            custom_colors = [[0.0, '#2563EB'], [1.0, '#10B981']] # Blue to Green
            fig = px.imshow(plot_df[numeric_cols_viz].corr(), text_auto=".2f", color_continuous_scale=custom_colors, aspect="auto")
            fig.update_layout(height=500, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == "Feature Distribution" and numeric_cols_viz:
            selected_col = st.selectbox("Select Feature:", numeric_cols_viz)
            fig = px.histogram(plot_df, x=selected_col, marginal="box", color_discrete_sequence=['#3B82F6'])
            fig.update_layout(height=500, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)
        elif chart_type == "Bivariate Scatter" and len(numeric_cols_viz) >= 2:
            col_x = st.selectbox("X-Axis Feature:", numeric_cols_viz, index=0)
            col_y = st.selectbox("Y-Axis Feature:", numeric_cols_viz, index=1 if len(numeric_cols_viz)>1 else 0)
            fig = px.scatter(plot_df, x=col_x, y=col_y, trendline="ols", color_discrete_sequence=['#10B981'])
            fig.update_layout(height=500, paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

    # --- VIEW 3: AI INSIGHT ENGINE & CHATBOT ---
    elif selected_view == "🤖 AI Insight & Chat":
        st.markdown("### 🧠 Preprocessing & Algorithmic Methodology")
        with st.expander("View System Decision Logic (Why these algorithms?)", expanded=False):
            st.markdown("""
            **Automated Imputation Engine Rules:**
            * **Numerical Matrices:** Handled via **Median Imputation**. Highly robust against outliers.
            * **Categorical Matrices:** Handled via **Mode Imputation**. Preserves class distributions.
            * **Vectorized Regex Filtering:** Hunts anomalies (e.g., '?', 'N/A') strictly within string matrices.
            """)
        
        st.divider()
        st.markdown("### 💬 Dynamic Data Assistant (Offline NLP Engine)")
        st.caption("Ask questions about specific columns. Try: 'What is the maximum of [column]?', 'Average of [column]?', or 'Unique values in [column]?'")
        
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
                            response_text = f"Column **{col}** is not numeric, so I cannot find a maximum."
                    elif any(word in prompt_lower for word in ['min', 'minimum', 'lowest']):
                        if pd.api.types.is_numeric_dtype(df[col]):
                            response_text = f"The minimum value in **{col}** is {df[col].min():.2f}."
                        else:
                            response_text = f"Column **{col}** is not numeric."
                    elif any(word in prompt_lower for word in ['mean', 'average', 'avg']):
                        if pd.api.types.is_numeric_dtype(df[col]):
                            response_text = f"The average (mean) value of **{col}** is {df[col].mean():.2f}."
                        else:
                            response_text = f"Column **{col}** is text/categorical. I cannot calculate an average."
                    elif any(word in prompt_lower for word in ['unique', 'distinct', 'categories']):
                        response_text = f"There are **{df[col].nunique()}** unique values in **{col}**. Here are the top occurrences:"
                        response_df = pd.DataFrame(df[col].value_counts().head(5))
                    else:
                        response_text = f"Here is a quick look at the data inside the **{col}** column:"
                        response_df = df[[col]].head(10)
                        
                elif any(word in prompt_lower for word in ['head', 'top', 'first']):
                    response_text = "Here are the top 5 rows of your dataset:"
                    response_df = df.head()
                elif any(word in prompt_lower for word in ['tail', 'bottom', 'last']):
                    response_text = "Here are the last 5 rows of your dataset:"
                    response_df = df.tail()
                elif any(word in prompt_lower for word in ['shape', 'size', 'row', 'column', 'coloum', 'coloumn', 'feature']):
                    response_text = f"Your dataset consists of **{df.shape[0]:,} rows** and **{df.shape[1]} columns**."
                elif any(word in prompt_lower for word in ['missing', 'null', 'empty']):
                    missing_count = df.isnull().sum().sum()
                    if missing_count == 0:
                        response_text = "Great news! Your dataset is completely clean with **0 missing values**."
                    else:
                        response_text = f"I detected **{missing_count:,} missing values** across the dataset. Please navigate to 'Profiling & Cleaning' to auto-clean them."
                else:
                    response_text = "🤖 *I am your offline Data NLP Engine.* Mention a specific column name (e.g. 'what is the average of [column]') or ask general questions like 'show missing values'."
                
                st.markdown(response_text)
                st.session_state.chat_history.append({"role": "assistant", "type": "text", "content": response_text})
                
                if response_df is not None:
                    st.dataframe(response_df)
                    st.session_state.chat_history.append({"role": "assistant", "type": "dataframe", "content": response_df})

    # --- VIEW 4: IEEE REPORT EXPORT ---
    elif selected_view == "📄 IEEE Report Export":
        st.markdown("### Publication-Ready Documentation")
        total_rows = df.shape[0]
        total_cols = df.shape[1]
        missing_vals = df.isnull().sum().sum()
        status_text = "Aggressively Cleaned & Imputed" if st.session_state.cleaned else "Raw, Uncleaned Data"
        num_cols_report = df.select_dtypes(include=[np.number]).columns.tolist()
        
        ieee_html = f"""
        <div style="font-family: 'Times New Roman', Times, serif; color: black; background: white; padding: 40px; border: 1px solid #ccc; max-width: 900px; margin: 0 auto; box-shadow: 0px 4px 10px rgba(0,0,0,0.1);">
            <h2 style="text-align: center; text-transform: uppercase; margin-bottom: 5px; font-size: 24px;">Automated Exploratory Data Analysis Report</h2>
            <p style="text-align: center; margin-top: 0px; margin-bottom: 30px; font-size: 16px;">
                <i>Generated by AI EDA Generator Platform</i><br>Group 16, Dept of Computer Science & Engineering (Data Science)<br>Inderprastha Engineering College (IPEC)
            </p>
            <div style="column-count: 2; column-gap: 40px; text-align: justify; font-size: 14px; line-height: 1.6;">
                <p><strong><em>Abstract</em>—This document presents an automated exploratory data analysis (EDA) of the ingested tabular dataset. The system dynamically profiled the structural integrity, missing values, and statistical distributions of the data to accelerate the preprocessing pipeline, effectively eliminating the manual overhead typically required by data scientists.</strong></p>
                <h4 style="text-align: center; text-transform: uppercase; margin-top: 20px; margin-bottom: 10px; font-size: 14px;">I. Introduction</h4>
                <p>Manual EDA is inherently time-consuming. This automated platform ingested a dataset comprising {total_rows:,} observations and {total_cols} features to rapidly identify data quality issues and statistical patterns.</p>
                <h4 style="text-align: center; text-transform: uppercase; margin-top: 20px; margin-bottom: 10px; font-size: 14px;">II. Data Profiling</h4>
                <ul style="margin-top: 0; padding-left: 20px;">
                    <li><strong>Total Observations:</strong> {total_rows:,}</li>
                    <li><strong>Dimensionality:</strong> {total_cols} features</li>
                    <li><strong>Missing Values:</strong> {missing_vals}</li>
                    <li><strong>Cleaning Status:</strong> {status_text}</li>
                </ul>
                <h4 style="text-align: center; text-transform: uppercase; margin-top: 20px; margin-bottom: 10px; font-size: 14px;">III. Statistical Results</h4>
        """
        if num_cols_report:
            ieee_html += "<ul style='margin-top: 0; padding-left: 20px;'>"
            for col in num_cols_report[:5]:
                ieee_html += f"<li><strong>{col}:</strong> Mean = {df[col].mean():.2f}, Std Dev = {df[col].std():.2f}</li>"
            ieee_html += "</ul>"
            
        ieee_html += f"""
                <h4 style="text-align: center; text-transform: uppercase; margin-top: 20px; margin-bottom: 10px; font-size: 14px;">IV. Conclusion</h4>
                <p>The dataset, '{st.session_state.last_file}', has been fully profiled. Based on the quality assessment, the data is {"ready" if st.session_state.cleaned else "not yet ready"} for model deployment.</p>
            </div>
        </div>
        """
        st.markdown(ieee_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.download_button(label="📥 Download IEEE Report (HTML Format)", data=ieee_html, file_name=f"IPEC_EDA_Report_{st.session_state.last_file.split('.')[0]}.html", mime="text/html", use_container_width=True)

    # --- VIEW 5: EXPORT CLEAN DATA ---
    elif selected_view == "💾 Export Clean Data":
        st.markdown("### 💾 Export Processed Dataset")
        st.write("Save the noise-free, fully imputed dataset directly to your machine.")
        
        if not st.session_state.cleaned:
            st.error("🛑 STOP! You cannot export this file yet. The dataset still contains missing values and anomalies.")
            st.warning("👉 Navigate to **🗄️ Profiling & Cleaning** in the sidebar and click the **'Execute Aggressive Auto-Clean'** button first.")
        else:
            st.success("✅ Dataset has been aggressively cleaned. It is strictly numeric/categorical with zero missing or garbage values.")
            
            st.info("⚡ High-Performance Offline Mode: To prevent browser lag with massive files, clicking the button below will instantly save the CSV directly to your local folder.")
            
            save_name = f"Cleaned_{st.session_state.last_file.split('.')[0]}.csv"
            
            if st.button("💾 Save Cleaned Data to Folder", use_container_width=True):
                with st.spinner("Writing dataset to disk..."):
                    try:
                        df.to_csv(save_name, index=False)
                        st.success(f"🎉 Success! You can now find '{save_name}' sitting alongside your app.py file.")
                        st.balloons()
                    except Exception as e:
                        st.error(f"Failed to save file: {e}")

else:
    st.info("👈 **System Standby:** Awaiting dataset ingestion. Please upload a file via the sidebar control panel.")
