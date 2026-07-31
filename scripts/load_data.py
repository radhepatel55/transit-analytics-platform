import pandas as pd
from pathlib import Path

# parent folder
SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"

df = pd.read_excel(DATA_DIR / "ttc-bus-delay-data-2024.xlsx")

# first 5 rows
print(df.head())

# basic info
print(df.info())

# total rows
print(f"Total rows: {len(df)}")

# rows where route is missing
print(df[df['Route'].isna()].head(10))

# rows where direction is missing
print(df[df['Direction'].isna()]['Incident'].value_counts())

# missing routes
print(df[df['Route'].isna()]['Incident'].value_counts())

# in missing routes, vehicle = 0 vs vehicle number
missing_route = df[df['Route'].isna()]
print(missing_route['Vehicle'].apply(lambda v: 'No Vehicle (0)' if v == 0 else 'Has Vehicle').value_counts())