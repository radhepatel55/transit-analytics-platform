import pandas as pd
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"

years = [2020, 2021, 2022, 2023, 2024]
all_years_data = []

column_rename_map = {
    "Report Date": "Date",
    "Delay": "Min Delay",
    "Gap": "Min Gap"
}

for year in years:
    file_path = DATA_DIR / f"ttc-bus-delay-data-{year}.xlsx"
    print(f"Loading {year}...")
    
    df_year = pd.read_excel(file_path)
    df_year = df_year.rename(columns=column_rename_map) 
    df_year["Year"] = year
    
    all_years_data.append(df_year)
    print(f"  {year}: {len(df_year)} rows loaded")

# combine all years in one table
combined = pd.concat(all_years_data, ignore_index=True)
print(f"\nTotal combined rows: {len(combined)}")

# drop empty rows 
print(f"\nBefore cleaning: {len(combined)} rows")
combined = combined.dropna(subset=['Route'])
print(f"After dropping missing Route: {len(combined)} rows")

# fill empty cells with NaN
combined['Direction'] = combined['Direction'].fillna('NaN')

# count of missing values (check)
print("\nMissing values remaining:")
print(combined.isna().sum())

combined.to_excel(DATA_DIR / "ttc-bus-delay-2020-2024-clean.xlsx", index=False)
print("\nSaved combined file!")