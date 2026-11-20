from datasets import load_dataset
import pandas as pd

print("Downloading VynFi Supply Chain dataset...")
print("This might take a minute or two...")

# Notice the comma and 'events' added below!
dataset = load_dataset("VynFi/vynfi-supply-chain-ocel", "events")

print("\nDataset Structure:")
print(dataset)

df = dataset['train'].to_pandas()

print("\nFirst 5 rows of the data:")
print(df.head())

print("\nColumn names:")
print(df.columns.tolist())

df.to_csv("data/raw/vynfi_supply_chain_events.csv", index=False)
print("\nSaved raw data to data/raw/vynfi_supply_chain_events.csv")
