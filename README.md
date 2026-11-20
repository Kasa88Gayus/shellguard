# ShellGuard

`ShellGuard` is an open-source research prototype designed to detect illicit shell-company and vendor-network fraud topologies. It models corporate ownership and event/transaction relationships and applies machine learning alongside explainability methods to flag suspicious entities and inspect risk drivers.

## Getting Started

Install dependencies and run the pipeline locally from the repository root:

```bash
pip install -r requirements.txt
python src/make_synthetic.py
python src/build_graph.py
python src/baseline_model.py
python src/explain_model.py
python src/gnn_model.py
streamlit run src/app.py
