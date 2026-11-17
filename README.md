# ShellGuard: Explainable Graph-Based Risk Engine

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


*(Notice the `##` before "Week 2 & 3 Updates". This makes it a proper heading, just like "Getting Started").*

Scroll down and click **Commit changes**.

---

### 📝 Step 2: Let's write the Research Paper (Methodology & Results)

You have all the technical results. Now we need to turn this into a document that a university admissions board will drool over. 

You don't need to write it from scratch. As a data scientist, you let the data write the story. We are going to create a `docs/paper_draft.md` file.

In your Ubuntu terminal, run:
```bash
nano docs/paper_draft.md

