"""Generate a synthetic beneficial-ownership graph with planted shell structures."""
import random
import pandas as pd
from pathlib import Path

# Set a seed so the data is the exact same every time we run it
random.seed(42)
OUT = Path("data/raw/synthetic")
OUT.mkdir(parents=True, exist_ok=True)

JURISDICTIONS = ["BVI", "Cayman", "Seychelles", "Panama", "Delaware", "UK", "Singapore"]
HIGH_RISK = {"BVI", "Cayman", "Seychelles", "Panama"}

def make_company(cid, jurisdiction, is_shell, nominee):
    return {
        "entity_id": cid,
        "entity_type": "company",
        "jurisdiction": jurisdiction,
        "is_shell": is_shell,
        "nominee_director": nominee,
        "incorporation_year": random.randint(1995, 2023),
    }

def main(n_legit=200, n_shell_chains=40):
    entities = []
    edges = []
    cid = 0

    # 1. Legitimate companies
    for _ in range(n_legit):
        cid += 1
        j = random.choice(["Delaware", "UK", "Singapore"])
        entities.append(make_company(f"C{cid}", j, False, False))

    # 2. Shell chains: owner -> shell -> shell -> operating vendor
    for chain in range(n_shell_chains):
        owner = f"O{chain}"
        entities.append({
            "entity_id": owner, "entity_type": "person",
            "jurisdiction": random.choice(list(HIGH_RISK)),
            "is_shell": False, "nominee_director": False,
            "incorporation_year": random.randint(1995, 2023),
        })
        prev = owner
        for depth in range(random.randint(2, 4)):
            cid += 1
            shell = make_company(
                f"C{cid}",
                random.choice(list(HIGH_RISK)),
                True,
                random.random() < 0.6,
            )
            entities.append(shell)
            edges.append({"source": prev, "target": f"C{cid}", "relation": "OWNS"})
            prev = f"C{cid}"
        cid += 1
        vendor = make_company(f"C{cid}", "Delaware", False, False)
        entities.append(vendor)
        edges.append({"source": prev, "target": f"C{cid}", "relation": "OWNS"})

    pd.DataFrame(entities).to_csv(OUT / "entities.csv", index=False)
    pd.DataFrame(edges).to_csv(OUT / "edges.csv", index=False)
    print(f"Success! Wrote {len(entities)} entities and {len(edges)} edges to {OUT}")

if __name__ == "__main__":
    main()
