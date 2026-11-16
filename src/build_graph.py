import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

# 1. Load the data we just generated
ent = pd.read_csv("data/raw/synthetic/entities.csv")
edg = pd.read_csv("data/raw/synthetic/edges.csv")

# 2. Build the directed graph
# Nodes will be entity_ids, edges will be the ownership relationships
G = nx.from_pandas_edgelist(edg, source="source", target="target",
                            edge_attr="relation", create_using=nx.DiGraph())

print(f"Graph built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

# 3. Calculate graph metrics for every node
print("Calculating metrics (this might take a few seconds)...")
betweenness = nx.betweenness_centrality(G)
pagerank = nx.pagerank(G)
degree = dict(G.degree())

# 4. Combine metrics into a DataFrame and merge with entity details
metrics = pd.DataFrame({
    "entity_id": list(G.nodes),
    "degree": [degree[n] for n in G.nodes],
    "betweenness": [betweenness[n] for n in G.nodes],
    "pagerank": [pagerank[n] for n in G.nodes],
})

# Merge with the entities data to get the 'is_shell' labels
metrics = metrics.merge(ent, on="entity_id", how="left")
metrics.to_csv("outputs/node_metrics.csv", index=False)
print("Saved metrics to outputs/node_metrics.csv")

# 5. Create our first visualization!
fig, ax = plt.subplots(figsize=(10, 6))

# Plot the distribution of betweenness for shells vs non-shells
for shell, group in metrics.groupby("is_shell"):
    label = "Illicit Shell" if shell else "Legitimate"
    color = "crimson" if shell else "steelblue"
    ax.hist(group["betweenness"], bins=30, alpha=0.6, label=label, color=color)

ax.set_xlabel("Betweenness Centrality (How often a node acts as a bridge)")
ax.set_ylabel("Number of Entities")
ax.set_title("Betweenness Centrality by Shell Status")
ax.legend()
plt.tight_layout()

# Save the figure
plt.savefig("outputs/fig01_betweenness_by_shell.png", dpi=150)
print("Saved chart to outputs/fig01_betweenness_by_shell.png")
