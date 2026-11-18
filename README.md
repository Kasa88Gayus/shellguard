# ShellGuard: Explainable Graph-Based Risk Engine

**🚀 [Launch the Live Interactive Dashboard](https://shellguard-forensics.streamlit.app)**

## Overview
ShellGuard is an open-source research prototype designed to detect illicit shell-company and vendor-network fraud topologies. It models corporate ownership structures as heterogeneous graphs and applies machine learning to flag suspicious entities.

## Research Question
Can hybrid graph-metric and Graph Neural Network (GNN) models detect shell-company structures more accurately, and more explainably, than traditional tabular methods?

## Current Status (Week 1)
- Built a synthetic data generator to simulate legitimate companies and hidden shell-ownership chains.
- Constructed a directed graph using `NetworkX`.
- Engineered graph-based forensic features (Degree, Betweenness Centrality, PageRank).
- Trained a baseline Random Forest model achieving perfect separation (ROC-AUC: 1.0000) on the synthetic benchmark.

## Project Structure
- `src/make_synthetic.py`: Generates the synthetic corporate network.
- `src/build_graph.py`: Constructs the graph and calculates node metrics.
- `src/baseline_model.py`: Trains the baseline machine learning model.

## Getting Started
```bash
pip install -r requirements.txt
python src/make_synthetic.py
python src/build_graph.py
python src/baseline_model.py

