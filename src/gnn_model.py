import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
from torch_geometric.data import Data
import pandas as pd
import networkx as nx
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

# 1. Load the network data
print("Loading graph data...")
ent = pd.read_csv("data/raw/synthetic/entities.csv")
edg = pd.read_csv("data/raw/synthetic/edges.csv")

# Create a mapping of entity IDs to integer indices
node_map = {id: i for i, id in enumerate(ent["entity_id"])}

# 2. Prepare Node Features (Degree)
G = nx.from_pandas_edgelist(edg, source="source", target="target", create_using=nx.DiGraph())
degree = dict(G.degree())

x = torch.tensor([[degree.get(id, 0)] for id in ent["entity_id"]], dtype=torch.float)
y = torch.tensor(ent["is_shell"].astype(int).values, dtype=torch.long)

# 3. Prepare the Edges
source_idx = [node_map[src] for src in edg["source"]]
target_idx = [node_map[tgt] for tgt in edg["target"]]
edge_index = torch.tensor([source_idx, target_idx], dtype=torch.long)

# Combine into a PyTorch Geometric Data object
data = Data(x=x, edge_index=edge_index, y=y)

# 4. Define the Graph Neural Network Architecture
class ShellGNN(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.conv1 = GCNConv(1, 16)
        self.conv2 = GCNConv(16, 2)

    def forward(self, data):
        x, edge_index = data.x, data.edge_index
        x = self.conv1(x, edge_index)
        x = F.relu(x)
        x = F.dropout(x, training=self.training)
        x = self.conv2(x, edge_index)
        return F.log_softmax(x, dim=1)

# 5. Train the Model
print("Training Graph Neural Network...")
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model = ShellGNN().to(device)
data = data.to(device)
optimizer = torch.optim.Adam(model.parameters(), lr=0.01, weight_decay=5e-4)

# Split data
train_mask, test_mask = train_test_split(range(len(y)), test_size=0.3, random_state=42, stratify=y)
train_mask_t = torch.zeros(len(y), dtype=torch.bool)
train_mask_t[train_mask] = True
test_mask_t = torch.zeros(len(y), dtype=torch.bool)
test_mask_t[test_mask] = True

data.train_mask = train_mask_t
data.test_mask = test_mask_t

model.train()
for epoch in range(200):
    optimizer.zero_grad()
    out = model(data)
    loss = F.nll_loss(out[data.train_mask], data.y[data.train_mask])
    loss.backward()
    optimizer.step()

# 6. Evaluate the Model
model.eval()
with torch.no_grad():
    out = model(data)
    probs = torch.exp(out[:, 1])
    test_labels = data.y[data.test_mask].cpu().numpy()
    test_probs = probs[data.test_mask].cpu().numpy()
    auc = roc_auc_score(test_labels, test_probs)
    print(f"\n--- GNN MODEL EVALUATION ---")
    print(f"GNN ROC-AUC Score: {auc:.4f}")
