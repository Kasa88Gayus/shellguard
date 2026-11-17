import streamlit as st
import pandas as pd
import io

# 1. Page configuration
st.set_page_config(page_title="ShellGuard", page_icon="🕵️‍♂️", layout="wide")

st.title("🕵️‍♂️ ShellGuard: Forensic Network Analytics")
st.markdown("""
Welcome to the ShellGuard Dashboard. 
Upload a corporate metrics dataset (CSV) to detect potential shell companies.
""")

# 2. Sidebar: File Uploader
st.sidebar.header("Upload Data")
uploaded_file = st.sidebar.file_uploader("Upload node_metrics.csv", type=["csv"])

# 3. Main Dashboard Logic
if uploaded_file is not None:
    try:
        # Read the uploaded CSV file
        df = pd.read_csv(uploaded_file)
        
        # Ensure it's only companies
        if "entity_type" in df.columns:
            df = df[df["entity_type"] == "company"]
        
        # Calculate metrics
        total_companies = len(df)
        flagged_shells = len(df[df["is_shell"] == 1]) if "is_shell" in df.columns else 0
        
        # KPI Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Companies Uploaded", total_companies)
        col2.metric("Flagged Shell Companies", flagged_shells)
        col3.metric("Model Status", "Active")
        
        st.divider()
        
        # Data Table
        st.subheader("High-Risk Entities (Top 5)")
        if "betweenness" in df.columns:
            top_risk = df.sort_values(by="betweenness", ascending=False).head(5)
            cols_to_show = [c for c in ["entity_id", "jurisdiction", "betweenness", "pagerank", "is_shell"] if c in df.columns]
            st.dataframe(top_risk[cols_to_show], use_container_width=True)
            
        # Display the SHAP image
        st.subheader("Explainable AI (SHAP)")
        try:
            st.image("outputs/fig03_shap_explanation.png", caption="Why was this entity flagged?")
        except FileNotFoundError:
            st.info("SHAP chart not found. Run explain_model.py to generate it.")
            
    except Exception as e:
        st.error(f"Error processing the file: {e}")
else:
    st.info("👈 Please upload a CSV file in the sidebar to begin analysis.")
