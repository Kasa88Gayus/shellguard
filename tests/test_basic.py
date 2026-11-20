import importlib.util
from pathlib import Path
import networkx as nx
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = REPO_ROOT / "src"


def _load_src_module(module_name: str):
    file_path = SRC_DIR / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    assert spec is not None and spec.loader is not None
    spec.loader.exec_module(module)
    return module


def test_graph_construction():
    data = {"source": ["A", "B"], "target": ["B", "C"]}
    df = pd.DataFrame(data)

    graph = nx.from_pandas_edgelist(
        df, source="source", target="target", create_using=nx.DiGraph()
    )

    assert graph.number_of_nodes() == 3
    assert graph.number_of_edges() == 2
    assert graph.has_edge("A", "B")
    assert not graph.has_edge("A", "C")


def test_make_company_fields():
    make_synthetic = _load_src_module("make_synthetic")
    company = make_synthetic.make_company(
        cid="C101",
        jurisdiction="Delaware",
        is_shell=True,
        nominee=False,
    )

    assert isinstance(company, dict)
    assert company["entity_id"] == "C101"
    assert company["jurisdiction"] == "Delaware"
    assert company["is_shell"] is True
