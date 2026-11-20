import pandas as pd
import networkx as nx
from pathlib import Path

def main():
    print("Loading real-world VynFi data...")
    # Load the raw dataset
    df = pd.read_csv("data/raw/vynfi_supply_chain_events.csv", low_memory=False)

    # 1. Fix the Labels (Convert True/False to 1/0)
    df['is_anomaly'] = df['is_anomaly'].astype(int)

    # 2. Extract Edges (Company <-> Company relationships only)
    edges_list = []

    # A. Company to Vendor
    vendors = df.dropna(subset=['company_code', 'attributes.vendor_id'])[['company_code', 'attributes.vendor_id']].copy()
    vendors.columns = ['source', 'target']
    edges_list.append(vendors)

    # B. Customer to Company
    customers = df.dropna(subset=['attributes.customer_id', 'company_code'])[['attributes.customer_id', 'company_code']].copy()
    customers.columns = ['source', 'target']
    edges_list.append(customers)

    # Combine and remove duplicates
    edges = pd.concat(edges_list, ignore_index=True).drop_duplicates()
    Path("outputs").mkdir(exist_ok=True)
    edges.to_csv("outputs/vynfi_edges.csv", index=False)
    print(f"Created {len(edges)} unique company-to-company relationships.")

    # 3. Build the Directed Graph
    G = nx.from_pandas_edgelist(edges, source='source', target='target', create_using=nx.DiGraph())
    print(f"Graph built with {G.number_of_nodes()} nodes.")

    # 4. Calculate Graph Metrics
    print("Calculating metrics (this might take a moment)...")
    degree = dict(G.degree())
    betweenness = nx.betweenness_centrality(G)
    pagerank = nx.pagerank(G)

    # 5. Create the Nodes DataFrame
    nodes = pd.DataFrame(list(G.nodes()), columns=['entity_id'])
    nodes['entity_type'] = 'company'
    nodes['degree'] = nodes['entity_id'].map(degree)
    nodes['betweenness'] = nodes['entity_id'].map(betweenness)
    nodes['pagerank'] = nodes['entity_id'].map(pagerank)

    # 6. Determine Labels (Direct Anomalies Only)
    # Extract entities directly involved in anomalous events
    anomalous_companies = set(df[df['is_anomaly'] == 1]['company_code'].dropna())
    anomalous_vendors = set(df[df['is_anomaly'] == 1]['attributes.vendor_id'].dropna())
    anomalous_customers = set(df[df['is_anomaly'] == 1]['attributes.customer_id'].dropna())
    
    direct_anomalies = anomalous_companies.union(anomalous_vendors).union(anomalous_customers)

    # Apply labels (We use 'is_shell' so the dashboard column names match)
    nodes['is_shell'] = nodes['entity_id'].apply(lambda x: 1 if x in direct_anomalies else 0)

    # 7. Save the Output
    nodes.to_csv("outputs/vynfi_node_metrics.csv", index=False)
    print("\nSuccess! Saved real-world graph data to outputs/")
    print(f"Total direct anomalies: {len(direct_anomalies)}")
    print(f"Total risky entities: {nodes['is_shell'].sum()} out of {len(nodes)}")

if __name__ == "__main__":
    main()
