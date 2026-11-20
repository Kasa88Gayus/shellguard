import streamlit as st
import pandas as pd
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

# 1. Page configuration
st.set_page_config(page_title="ShellGuard", page_icon="🕵️‍♂️", layout="wide")

st.title("🕵️‍♂️ ShellGuard: Forensic Network Analytics")
st.markdown("""
Welcome to the ShellGuard Dashboard. 
Upload your corporate metrics and edge data to visualize the network and detect shell companies.
""")

# 2. Sidebar: File Uploaders
st.sidebar.header("Upload Data")
metrics_file = st.sidebar.file_uploader("1. Upload node_metrics.csv", type=["csv"])
edges_file = st.sidebar.file_uploader("2. Upload edges.csv (for graph)", type=["csv"])

# 3. Main Dashboard Logic
if metrics_file is not None:
    try:
        # Read the uploaded CSV file
        df = pd.read_csv(metrics_file)
        
        if "entity_type" in df.columns:
            df = df[df["entity_type"] == "company"]
        
        total_companies = len(df)
        flagged_shells = len(df[df["is_shell"] == 1]) if "is_shell" in df.columns else 0
        
        # KPI Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Companies Uploaded", total_companies)
        col2.metric("Flagged Shell Companies", flagged_shells)
        col3.metric("Model Status", "Active")
        
        st.divider()
        
        # Layout
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("High-Risk Entities (Top 5)")
            if "betweenness" in df.columns:
                top_risk = df.sort_values(by="betweenness", ascending=False).head(5)
                cols_to_show = [c for c in ["entity_id", "jurisdiction", "betweenness", "is_shell"] if c in df.columns]
                st.dataframe(top_risk[cols_to_show], use_container_width=True)
                
        with col_right:
            st.subheader("Explainable AI (SHAP)")
            try:
                st.image("fig03_shap_explanation.png", caption="Why was this entity flagged?")
            except Exception:
                st.info("SHAP chart not found.")
        
        # 4. INTERACTIVE NETWORK GRAPH
        if edges_file is not None:
            st.divider()
            st.subheader("🕸️ Interactive Network Graph")
            st.markdown("Drag nodes to explore. **Red** = Shell Company, **Blue** = Legitimate.")
            
            # Load edges
            edg = pd.read_csv(edges_file)
            
            # Create network graph
            G = nx.from_pandas_edgelist(edg, source="source", target="target", create_using=nx.DiGraph())
            
            # Initialize PyVis
            net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white", directed=True)
            net.from_nx(G)
            
            # Color nodes based on whether they are a shell company
            shell_dict = dict(zip(df["entity_id"], df["is_shell"]))
            
            for node in net.nodes:
                node_id = node["id"]
                if shell_dict.get(node_id) == 1:
                    node["color"] = "#ff4b4b" # Red for shell
                    node["size"] = 25
                    node["title"] = "High Risk: Shell Company"
                else:
                    node["color"] = "#4b88ff" # Blue for legit
                    node["size"] = 15
                    node["title"] = "Legitimate Entity"
            
            # Save and display the graph
            net.save_graph("outputs/network_graph.html")
            
            # Embed the HTML in Streamlit
            with open("outputs/network_graph.html", 'r', encoding='utf-8') as f:
                html_data = f.read()
            components.html(html_data, height=620)

    except Exception as e:
        st.error(f"Error processing the file: {e}")
else:
    st.info("👈 Please upload the node_metrics.csv file in the sidebar to begin analysis.")
