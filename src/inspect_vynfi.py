import pandas as pd

# Load the data
df = pd.read_csv("data/raw/vynfi_supply_chain_events.csv")

print("=== 1. What does 'is_anomaly' look like? ===")
print(df['is_anomaly'].value_counts(dropna=False))

print("\n=== 2. What are the most common event types (activity_name)? ===")
print(df['activity_name'].value_counts().head(10))

print("\n=== 3. Are there vendor IDs in these events? ===")
# Count how many rows actually have a vendor ID (not empty)
valid_vendors = df['attributes.vendor_id'].dropna()
print(f"Total rows: {len(df)}")
print(f"Rows with a Vendor ID: {len(valid_vendors)}")

print("\n=== 4. Let's look at a few rows that DO have a vendor ID ===")
sample_with_vendor = df[df['attributes.vendor_id'].notna()][['company_code', 'attributes.vendor_id', 'activity_name', 'is_anomaly']].head(5)
print(sample_with_vendor)
