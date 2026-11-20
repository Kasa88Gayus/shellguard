---
title: 'ShellGuard: An Explainable Graph-Based Risk Engine for Forensic Detection of Shell Companies'
tags:
  - Python
  - forensic accounting
  - financial crime
  - graph neural networks
  - explainable AI
  - anti-money laundering
authors:
  - name: Yohanna Kasa
    affiliation: 1
affiliations:
  - name: Anti-Money Laundering and Transaction Compliance Specialist
    index: 1
date: 2026-11-20
bibliography: paper.bib
---

# Summary

`ShellGuard` is an open-source Python research prototype and interactive web application designed to detect illicit shell-company and vendor-network fraud topologies. It models corporate ownership and transaction/event relationships as graphs and applies both traditional machine learning (Random Forest) and Graph Neural Networks (GNNs) to score suspicious entities [@hagberg2008networkx; @paszke2019pytorch]. To support auditable and transparent investigative reviews, `ShellGuard` integrates SHAP (SHapley Additive exPlanations) to provide case-level feature attributions for risk predictions [@lundberg2017shap], alongside a `Streamlit` dashboard for interactive visual exploration [@streamlit].

# Statement of need

Illicit financial networks frequently obscure beneficial ownership and transaction flows across multi-layered corporate entities, intermediaries, and vendor chains. Traditional rule-based compliance alerts and static tabular reviews often struggle to capture structural network patterns across entities, while opaque anomaly scoring can make findings harder to audit or explain during investigative and regulatory reviews.

Researchers, forensic accountants, and anti-money laundering (AML) analysts need open, reproducible tooling that links graph-based representation learning with model explainability and visual inspection. `ShellGuard` addresses this need by providing a modular Python pipeline and `Streamlit` interface that compare tabular graph-feature classification against GNN-based risk scoring while generating SHAP explanations [@hagberg2008networkx; @paszke2019pytorch; @lundberg2017shap; @streamlit].

# State of the field

General-purpose graph libraries such as `NetworkX` [@hagberg2008networkx] and deep learning frameworks such as `PyTorch` [@paszke2019pytorch] provide core graph and neural network building blocks, but require custom integration to assemble forensic risk scoring, SHAP-based explanations [@lundberg2017shap], and interactive web inspection [@streamlit] for financial network investigations. Commercial intelligence platforms offer proprietary graph analysis and entity intelligence capabilities, but their closed nature and licensing costs limit transparent inspection and reproducible academic benchmarking.

`ShellGuard` provides an open-source research workflow combining synthetic data generation, graph feature engineering, Random Forest and GNN modeling, SHAP explainability, and an interactive `Streamlit` application in one repository.

# Software design

`ShellGuard` separates data preparation, graph construction, model training, explainability, and visualization into modular scripts under `src/` and an interactive dashboard at the root:

- **Synthetic Data Generation (`src/make_synthetic.py`):** Generates synthetic corporate ownership and vendor-network datasets representing legitimate entities and shell-company structures for controlled experimentation.
- **Graph Construction (`src/build_graph.py`):** Constructs graph representations from entity and event/transaction records using `NetworkX` [@hagberg2008networkx] and computes structural graph metrics (such as degree, betweenness centrality, and PageRank) alongside tabular/relational attributes.
- **Baseline & GNN Modeling (`src/baseline_model.py`, `src/gnn_model.py`):** Trains a Random Forest baseline on engineered features and a GNN model (`PyTorch` / graph neural layers) [@paszke2019pytorch] to estimate entity risk scores and write evaluation outputs to `outputs/`.
- **Explainability (`src/explain_model.py`):** Computes SHAP values [@lundberg2017shap] to explain feature contributions behind model risk predictions.
- **Interactive Dashboard (`src/app.py`):** Delivers a `Streamlit` web application [@streamlit] for exploring risk scores, explanations, and fraud topologies interactively.

# Research impact statement

`ShellGuard` was evaluated on both a synthetic corporate ownership dataset and the VynFi Supply Chain OCEL dataset. On the synthetic benchmark, the Random Forest baseline achieved a ROC-AUC of `1.0000` and the GNN achieved a ROC-AUC of `0.9377`; researchers interpreting a `1.0000` synthetic score should account for synthetic data separability, dataset size, and validation split design. On the VynFi Supply Chain OCEL dataset, the pipeline processed 320,000 rows and isolated a suspicious fraud ring within a 105-node network, illustrating practical utility for exploratory forensic analysis and AML research.

# AI usage disclosure

Generative AI (Google Gemini) was used to assist with boilerplate code for data processing and the `Streamlit` dashboard, as well as initial drafting of sections of this manuscript. All AI-generated code and text were reviewed, tested, edited, and verified for accuracy by the author.

# Acknowledgements

The author thanks the open-source community and maintainers of `NetworkX` [@hagberg2008networkx], `PyTorch` [@paszke2019pytorch], `SHAP` [@lundberg2017shap], and `Streamlit` [@streamlit], as well as supporting Python data and machine learning libraries used in this project.

# References
