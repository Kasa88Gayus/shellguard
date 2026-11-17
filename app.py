import streamlit as st
import pandas as pd

# 1. Page configuration
st.set_page_config(page_title="ShellGuard", page_icon="🕵️‍♂️", layout="wide")

# 2. Title and description
st.title("🕵️‍♂️ ShellGuard: Forensic Network Analytics")
st.markdown("""
Welcome to the ShellGuard Dashboard. 
This tool analyzes corporate ownership networks to detect potential shell companies using machine learning and graph theory.
""")

# 3. Sidebar controls
st.sidebar.header("Data Controls")
if st.sidebar.button("Load Project Data"):
    st.session_state['data_loaded'] = True

# 4. Main dashboard logic
if st.session_state.get('data_loaded', False):
    try:
        # Load the metrics we generated earlier
        df = pd.read_csv("outputs/node_metrics.csv")
        df = df[df["entity_type"] == "company"]
        
        # Top KPI metrics
        total_companies = len(df)
        flagged_shells = len(df[df["is_shell"] == 1])
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Companies Analyzed", total_companies)
        col2.metric("Flagged Shell Companies", flagged_shells)
        col3.metric("Model ROC-AUC", "1.0000")
        
        st.divider()
        
        # Layout for data table and chart
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("High-Risk Entities (Top 5)")
            # Sort by betweenness (highest risk) and show top 5
            top_risk = df.sort_values(by="betweenness", ascending=False).head(5)
            st.dataframe(top_risk[["entity_id", "jurisdiction", "betweenness", "pagerank", "is_shell"]], use_container_width=True)
            
        with col_right:
            st.subheader("Explainable AI (SHAP)")
            st.markdown("Why was this entity flagged?")
            # Display the SHAP image we just generated!
            st.image("outputs/fig03_shap_explanation.png", use_container_width=True)
            
    except FileNotFoundError:
        st.error("Data not found! Please run the Python scripts in the `src` folder first to generate the data.")
else:
    st.info("👈 Click 'Load Project Data' in the sidebar to start.")
