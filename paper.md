---
title: 'ShellGuard: An Explainable Graph-Based Risk Engine for Forensic Detection of Shell Companies'
tags:
  - Python
  - forensic accounting
  - financial crime
  - graph neural networks
  - explainable AI
authors:
  - name: Yohanna Kasa
    orcid: 0000-0000-0000-0000 # Replace with your ORCID if you have one
    affiliation: 1
affiliations:
  - name: Independent Researcher
    index: 1
date: 20 November 2026
bibliography: paper.bib
---

# Summary
`ShellGuard` is an open-source Python tool designed for forensic accountants, auditors, and financial crime researchers. It leverages graph theory and machine learning to detect illicit shell companies and hidden vendor networks within complex corporate structures. The tool models ownership and transaction data as a directed graph and applies both traditional machine learning (Random Forest) and cutting-edge deep learning (Graph Neural Networks) to identify suspicious entities. To ensure its findings are legally defensible and auditable, `ShellGuard` integrates SHAP (SHapley Additive exPlanations) to provide transparent, case-level justifications for every risk score it generates. The software includes an interactive Streamlit dashboard that allows users to visualize these fraud topologies in real-time.

# Statement of need
Traditional financial audits and rule-based systems are often ill-equipped to trace the complex, multi-layered ownership webs used in modern financial crime. These systems fail to capture the relational complexity of hidden networks. `ShellGuard` addresses this gap by providing an explainable, graph-based machine learning framework specifically tailored for forensic accounting. Its primary audience is forensic accountants and investigators who require not only high detection accuracy but also transparent reasoning to defend their findings in regulatory or legal contexts.

# State of the field
While general-purpose graph analytics libraries like `NetworkX` and `igraph` exist, they lack domain-specific tooling for forensic accounting. Commercial platforms (e.g., Sayari Graph) exist but are proprietary, opaque, and expensive. `ShellGuard` is unique in its combination of a user-friendly web dashboard, a dual-model architecture (traditional ML and GNNs), and a built-in explainability layer (SHAP), making it a complete, open-source solution for research and practical investigation.

# Software design
The software is designed for modularity and reproducibility. The core pipeline is written in Python and structured into distinct scripts for data generation (`make_synthetic.py`), graph construction (`build_graph.py`), model training (`baseline_model.py`, `gnn_model.py`), and explainability (`explain_model.py`). The interactive dashboard is built with Streamlit (`app.py`), allowing users to upload their own CSV data and visualize results without writing code. The architecture separates the data processing, modeling, and visualization layers, ensuring that the tool can be easily extended or integrated into other analytical pipelines.

# Research impact statement
`ShellGuard` was validated on both a synthetic corporate ownership network and the real-world VynFi Supply Chain dataset. On the synthetic benchmark, the Random Forest baseline achieved a perfect ROC-AUC of 1.0000, and the Graph Neural Network achieved a robust 0.9377. On the real-world dataset, the pipeline processed over 320,000 event-log rows to successfully isolate a high-risk fraud ring within a network of 105 nodes. The live dashboard demonstrates its immediate utility for research and education.

# AI usage disclosure
Generative AI (Google Gemini) was used to assist in the development of the software, specifically in writing boilerplate code for data processing and the Streamlit dashboard. All AI-generated code was reviewed, tested, and verified for correctness by the author. The AI was also used to assist in drafting the text of this paper, which was subsequently edited and verified by the author.

# Acknowledgements
The author would like to thank the open-source community for the development of the Python libraries used in this project, including Pandas, NetworkX, PyTorch, PyTorch Geometric, SHAP, and Streamlit.

# References
