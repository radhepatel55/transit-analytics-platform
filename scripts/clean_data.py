import pandas as pd
from pathlib import Path

# parent folder
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"

df = pd.read_excel(DATA_DIR / "ttc-bus-delay-data-2024.xlsx")

print(f"Starting rows: {len(df)}")

# drop rows where route is missing
df = df.dropna(subset=['Route'])

print(f"After dropping missing Route: {len(df)}")

# fill missing direction cells with NaN
df['Direction'] = df['Direction'].fillna('NaN')

# check for more missing values
print("\nMissing values remaining per column:")
print(df.isna().sum())

# save a cleaned file
df.to_excel(DATA_DIR / "ttc-bus-delay-data-2024-clean.xlsx", index=False)
print("\nSaved cleaned file!")