import pandas as pd
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
DATA_DIR = SCRIPT_DIR.parent / "data"

# create one row for every date from jan 2020 to dec 2024
date_range = pd.date_range(start="2020-01-01", end="2025-12-31", freq="D")

calendar = pd.DataFrame({"Date": date_range})

# Add descriptive columns names
calendar["Year"] = calendar["Date"].dt.year
calendar["Month"] = calendar["Date"].dt.month
calendar["MonthName"] = calendar["Date"].dt.strftime("%B")
calendar["Quarter"] = calendar["Date"].dt.quarter
calendar["DayOfWeek"] = calendar["Date"].dt.strftime("%A")
calendar["IsWeekend"] = calendar["Date"].dt.dayofweek >= 5
calendar["YearMonth"] = calendar["Date"].dt.strftime("%Y-%m")

print(f"Calendar table: {len(calendar)} rows")
print(calendar.head())

calendar.to_excel(DATA_DIR / "calendar_dim.xlsx", index=False)
print("\nSaved calendar table!")