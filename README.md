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

<img width="1415" height="232" alt="Image" src="https://github.com/user-attachments/assets/60e6aa91-a164-4b32-8c2e-366fc076931c" /> 


## Tech Stack

| Layer | Tool | Purpose |
|---|---|---|
| Ingestion | Python, pandas | Load and inspect raw TTC delay data |
| Data cleaning | pandas | Handle missing values, standardize schemas across years |
| Object storage | MinIO (S3-compatible) | Durable storage, mirrors real AWS S3 API via boto3 |
| Orchestration | Apache Airflow (Docker) | Automates the single-year ingestion pipeline on a schedule |
| Distributed processing | Databricks, PySpark | Scalable aggregation and analysis |
| Data warehouse | Snowflake | Central store for clean, query-ready tables |
| Visualization | Power BI | Interactive dashboard for stakeholders |

## Dataset

Source: [City of Toronto Open Data Portal](https://open.toronto.ca) — TTC Bus Delay Data, 2020–2024 (five full calendar years, ~180,000 cleaned records).

**Data quality notes** (documented, not hidden — this is real open government data with real quirks):
- 2020's file used different column names (`Report Date`, `Delay`, `Gap`) than 2021-2024 (`Date`, `Min Delay`, `Min Gap`) —> resolved with a column-standardization step.
- Rows missing a `Route` value (~1%) were dropped, since delays can't be attributed to a specific route without one —> investigated and found to correlate with high-stress incident types (collisions, security events) where the route number was likely skipped during logging.
- Missing `Direction` values were filled as `"NaN"` rather than dropped, since direction wasn't essential to the core analysis questions.
- 2025 data was evaluated but excluded from this version: TTC changed its incident classification system that year (categorical `Incident` labels replaced with internal `Code` values), and a reliable bus-specific code dictionary could not be confirmed. Noted as a candidate for a future update.

## Pipeline Stages

1. **Ingest** — load raw yearly `.xlsx` files with pandas
2. **Clean** — standardize schemas across years, handle missing values, validate assumptions against the data rather than guessing
3. **Store** — upload cleaned data to S3-compatible object storage (MinIO)
4. **Orchestrate** — Airflow DAG automates load → clean → upload for the recurring single-year pipeline, running in Docker with a Postgres metadata store and Celery executor
5. **Analyze** — PySpark aggregations across five dimensions: route, hour of day, incident type, day of week, and location
6. **Warehouse** — clean summary and fact tables loaded into Snowflake
7. **Visualize** — Power BI dashboard connected live to Snowflake

## Dashboard

![TTC Transit Analytics Dashboard](./dashboard/dashboard_screenshot.png)

*Screenshot of the Power BI dashboard.*

### Dashboard Pages

**Page 1 — Overview**
*(screenshot: `./dashboard/page1_overview.png`)*
High-level summary view — KPI cards for total incidents and average delay, worst routes by average delay, and delay severity by hour of day. Answers "what's happening overall?" at a glance.

**Page 2 — [add title]**
*(screenshot: `./dashboard/page2_....png`)*
[Describe what this page shows and what question it answers]

**Page 3 — [add title]**
*(screenshot: `./dashboard/page3_....png`)*
[Describe what this page shows and what question it answers]

## Key Findings

- **Route 77** has the highest average delay (136 min) among routes with a statistically meaningful incident count (60+ incidents)
- **7 AM** is a sharp, isolated delay spike — notably worse than the surrounding morning rush hour, and worse than the evening rush entirely
- **Diversions** are the single largest driver of severe delays (118.8 min average, 4,464 incidents) — far more impactful than mechanical failures or collisions
- **Jane and Steeles** and the surrounding northwest-Toronto corridor show a recurring cluster of high-delay locations
- Day-of-week has only a mild effect on delay severity (Monday 22.8 min vs. Saturday 20.0 min avg) — a useful negative finding, not every dimension needs to show a dramatic pattern

## Notes on Scope

Airflow orchestration was built and validated on the recurring single-year (2024) ingestion pipeline. The 2020-2024 historical backfill was performed as a one-time batch process rather than through Airflow, since automating a non-recurring task adds engineering overhead without operational benefit — a deliberate scope decision, not a shortcut.

## Setup

See `/scripts` for individual pipeline steps, `/airflow` for the DAG and Docker Compose configuration, and `/notebooks` for the PySpark analysis notebook.
