# TTC Transit Analytics Platform

This is an end-to-end data engineering pipeline that ingests, cleans, transforms, and visualizes Toronto Transit Commission (TTC) bus delay data and it is built to demonstrate the full modern data stack, from raw files all the way to an executive dashboard.

## Overview

This project answers real operational questions that a TTC transit planner might ask:

- Which bus routes experience the most severe delays?
- What time of day sees the worst reliability?
- Which incident types drive the biggest delays?
- Which locations are recurring problem spots?
- How does reliability vary by day of week?

## Architecture

<img width="1348" height="755" alt="image" src="https://github.com/user-attachments/assets/cf51d4d4-0890-4516-b8d3-73d2b1fff5ee" />


## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Ingestion | Python, pandas | Load and inspect raw TTC delay data |
| Data cleaning | pandas | Handle missing values, standardize schemas across years |
| Object storage | MinIO (S3-compatible) | Durable storage, mirrors real AWS S3 API via boto3 |
| Orchestration | Apache Airflow (Docker) | Automates the single-year ingestion pipeline on a schedule |
| Distributed processing | Databricks, PySpark | Scalable aggregation and analysis |
| Data warehouse | Snowflake | Star schema: `DELAYS` fact table + `CALENDAR` dimension, joined on Date |
| Visualization | Power BI | Interactive dashboard for stakeholders |

## Dataset

Source: [City of Toronto Open Data Portal](https://open.toronto.ca) — TTC Bus Delay Data, 2020–2024 (five full calendar years, 180,075 cleaned records).

**Data quality notes** (documented, not hidden — this is real open government data with real quirks):
- 2020's file used different column names (`Report Date`, `Delay`, `Gap`) than 2021-2024 (`Date`, `Min Delay`, `Min Gap`) — resolved with a column-standardization step.
- Rows missing a `Route` value (~1%) were dropped, since delays can't be attributed to a specific route without one — investigated and found to correlate with high-stress incident types (collisions, security events) where the route number was likely skipped during logging.
- Missing `Direction` values were filled as `"Unknown"` rather than dropped, since direction wasn't essential to the core analysis questions.
- 20 rows (0.011%) had a column-shift caused by unescaped commas in the `Location` field during CSV parsing (detectable by stray numeric values landing in `Direction`); identified via pattern matching and excluded rather than reconstructed, given the negligible volume.
- `Route` is stored as text (not numeric) in the warehouse, since some route codes are alphanumeric (e.g. `YU`), which an early numeric-type assumption briefly broke.
- 2025 data was evaluated but excluded from this version: TTC changed its incident classification system that year (categorical `Incident` labels replaced with internal `Code` values), and a reliable bus-specific code dictionary could not be confirmed. Noted as a candidate for a future update.

## Pipeline Stages

1. **Ingest** — load raw yearly `.xlsx`/`.csv` files with pandas
2. **Clean** — standardize schemas across years, handle missing values, validate assumptions against the data rather than guessing
3. **Store** — upload cleaned data to S3-compatible object storage (MinIO)
4. **Orchestrate** — Airflow DAG automates load → clean → upload for the recurring single-year pipeline, running in Docker with a Postgres metadata store and Celery executor
5. **Combine & model** — 2020-2024 yearly files combined into one 180,095-row dataset in PySpark; a separate Calendar dimension table (1,827 rows: one per day, with Year/Month/Quarter/DayOfWeek/IsWeekend) generated to support proper date-based analysis
6. **Warehouse** — loaded into Snowflake as a star schema: `DELAYS` fact table joined to `CALENDAR` dimension via a primary/foreign key relationship on Date
7. **Visualize** — Power BI connects live to Snowflake, aggregating directly off the fact table (not pre-computed summaries), enabling proper Top-N filtering and cross-chart interactivity

## Dashboard

![TTC Transit Analytics Dashboard](./dashboard/dashboard_screenshot.png)

*Screenshot of the Power BI dashboard.*

### Dashboard Pages

**Page 1 — Overview**
*<img width="1162" height="651" alt="image" src="https://github.com/user-attachments/assets/07a201c5-592f-490a-a424-678afdcfba29" />*
High-level summary view — four KPI cards (Total Delay Incidents, Average Delay, Longest Single Delay, Routes Impacted), worst routes by average delay (Route 174 highest among routes with a meaningful incident count), and delay severity by hour of day. Answers "what's happening overall?" at a glance.

**Page 2 — Operational Analysis**
*<img width="1162" height="652" alt="image" src="https://github.com/user-attachments/assets/e0b837ca-cd1a-41ea-914d-4456e781a276" />*
An investigative view for digging into specifics — a monthly delay trend line (2020–2024) built on the Calendar dimension table, a Top 15 worst-locations table, a date range slicer, and a Route slicer that cross-filters the whole page. Two comparison cards (Selected Route Avg Delay vs. System-Wide Avg Delay, the latter using a `CALCULATE`/`ALL` DAX measure to stay fixed regardless of filter) let a viewer judge whether a chosen route is actually worse than typical. Selecting Route 77 shows its specific locations, trend, and how it compares to the system average. Answers "where and when is this happening, and is it actually a problem?"

**Page 3 — Insights**
*<img width="1157" height="652" alt="image" src="https://github.com/user-attachments/assets/c20dc527-f2a5-4dda-a445-347684ccc0f1" />*
Root-cause view — incident type breakdown (Diversions stand out as the largest driver of severe delays), average delay by day of week (correctly ordered Monday–Sunday via a `WEEKDAY()`-based sort column), and a written insights callout summarizing the key takeaways and the 2020–2024 trend: delays were higher and more volatile in 2020–2021 (peaking ~26 min), stabilized into an 18–24 min range from 2022 onward, with a modest uptick in early 2024 worth monitoring. Answers "why is this happening, and what should management watch?"

## Key Findings

*Based on the full 2020–2024 dataset (180,075 cleaned records).*

- **~180,075 total delay incidents** across the 5-year period, averaging **20.64 minutes** per incident
- **Route 77** has the highest average delay among routes with a statistically meaningful incident count — flagged for operational review
- **7 AM** shows a visible delay spike relative to surrounding hours — worth additional resourcing during this window
- **Diversions** are the single largest driver of severe delays — far more impactful than mechanical failures or collisions
- Delay severity has **generally improved and stabilized** since 2020: volatile 2020–2021 peaks (~26 min) settled into a steadier 18–24 min range from 2022 onward, with a modest uptick in early 2024 worth continued monitoring
- Day-of-week has only a mild effect on delay severity — a useful negative finding, not every dimension needs to show a dramatic pattern

## Notes on Scope

Airflow orchestration was built and validated on the recurring single-year (2024) ingestion pipeline. The 2020-2024 historical backfill was performed as a one-time batch process rather than through Airflow, since automating a non-recurring task adds engineering overhead without operational benefit — a deliberate scope decision, not a shortcut.

## Setup

See `/scripts` for individual pipeline steps, `/airflow` for the DAG and Docker Compose configuration, and `/notebooks` for the PySpark analysis notebook.
