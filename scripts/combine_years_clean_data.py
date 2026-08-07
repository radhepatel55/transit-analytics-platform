import pandas as pd
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"

years = [2020, 2021, 2022, 2023, 2024, 2025]
all_years_data = []

column_rename_map = {
    "Report Date": "Date",
    "Delay": "Min Delay",
    "Gap": "Min Gap"
}

for year in years:
    if year == 2025:
        file_path = DATA_DIR / f"ttc-bus-delay-data-{year}.csv"
        df_year = pd.read_csv(file_path)
    else:
        file_path = DATA_DIR / f"ttc-bus-delay-data-{year}.xlsx"
        df_year = pd.read_excel(file_path)
    
    print(f"Loading {year}...")
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

combined.to_excel(DATA_DIR / "ttc-bus-delay-2020-2025-clean.xlsx", index=False)
print("\nSaved combined file!")