# ShellGuard: An Explainable Graph-Based Risk Engine for Forensic Detection of Shell Companies and Vendor Networks

## Abstract
The detection of illicit shell companies and hidden vendor networks is a critical challenge in forensic accounting. Traditional rule-based systems fail to capture the relational complexity of modern financial crime. This study introduces ShellGuard, a dual-model framework leveraging graph-theoretic metrics and Graph Neural Networks (GNNs) to detect shell entities. Evaluated on a synthetic corporate ownership network, the baseline Random Forest model achieved perfect classification (ROC-AUC: 1.0000), while a PyTorch Geometric GCN achieved a robust 0.9377 ROC-AUC. Furthermore, we integrate SHAP (SHapley Additive exPlanations) to provide legally defensible explanations for model predictions, bridging the gap between machine learning accuracy and forensic accountability.

## 1. Introduction
Money laundering and tax evasion frequently utilize "shell companies"—legal entities with no active business operations or significant assets. These entities are structured in complex, multi-layered ownership chains to obfuscate the Ultimate Beneficial Owner (UBO). Traditional financial audits struggle to scale to these network-based frauds. This project proposes a data science framework that models corporate structures as heterogeneous graphs to identify the structural motifs indicative of financial crime.

## 2. Methodology
### 2.1 Data Generation
Due to the confidential nature of real-world financial crime data, we developed a synthetic data generator (`src/make_synthetic.py`) simulating a corporate ecosystem of 404 entities. The dataset comprises 200 legitimate companies and 40 malicious "shell chains," where each chain features an Ultimate Beneficial Owner routing through 2 to 4 high-risk jurisdictions (e.g., BVI, Cayman Islands, Panama) before acquiring a legitimate vendor.

### 2.2 Graph Construction and Feature Engineering
The dataset was modeled as a directed graph using `NetworkX`. For each node, we engineered three forensic features:
- **Degree:** The number of direct connections (owners and subsidiaries).
- **Betweenness Centrality:** The frequency at which a node acts as a bridge between other nodes.
- **PageRank:** The relative structural importance of the entity within the network.

### 2.3 Machine Learning Models
We evaluated two distinct architectures:
1. **Random Forest Baseline (Tabular):** A tree-based ensemble model trained on the engineered graph metrics.
2. **Graph Neural Network (Relational):** A two-layer Graph Convolutional Network (GCN) implemented in `PyTorch Geometric`, designed to learn structural node embeddings by passing messages between connected entities.

### 2.4 Explainable AI (XAI)
To ensure forensic defensibility, we utilized `SHAP` (SHapley Additive exPlanations) to decompose the Random Forest's predictions, generating case-level waterfall charts to explain *why* an entity was flagged.

## 3. Results and Discussion
The Random Forest baseline achieved an ROC-AUC of 1.0000 on the synthetic test set. The SHAP analysis revealed that `degree` and `betweenness` were the most critical indicators; shell companies typically exhibit a degree of exactly 2 (one owner, one vendor) and zero betweenness (strictly linear chains). 

The Graph Neural Network achieved an ROC-AUC of 0.9377. While slightly lower than the tabular baseline, the GNN's ability to learn structural graph embeddings suggests it may generalize better to unseen, messy real-world data where hardcoded rules fail. 

## 4. Conclusion
The ShellGuard framework demonstrates that combining graph theory, traditional machine learning, and deep learning provides a highly accurate and explainable methodology for forensic accounting. Future work will involve validating the GNN model on real-world corporate registry data and deploying the Streamlit dashboard for live investigator use.
