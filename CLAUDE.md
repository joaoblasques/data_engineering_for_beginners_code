# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

This is a data engineering educational repository for the "Data Engineering for Beginners" e-book. It contains two distinct environments:

1. **Jupyter/Spark environment** (root level) - for SQL, Python, and data modeling tutorials
2. **Airflow/dbt environment** (`airflow/` directory) - for orchestration, transformation, and analytics pipelines

The project uses the TPC-H benchmark dataset (a standard decision support benchmark) to demonstrate data engineering concepts.

## Architecture

### Two Separate Docker Environments

The repository has two mutually exclusive Docker environments that **cannot run simultaneously**:

#### 1. Jupyter/Spark Environment (Root)
- **Stack**: Spark-Iceberg, MinIO (S3-compatible storage), Iceberg REST catalog
- **Purpose**: Interactive data exploration via Jupyter notebooks
- **Storage**: Iceberg tables in MinIO object storage
- **Access**: Jupyter at http://localhost:8888

#### 2. Airflow/dbt Environment (`airflow/`)
- **Stack**: Apache Airflow, dbt, Spark with Hive metastore, PostgreSQL, MinIO, Metabase
- **Purpose**: Production-style data pipelines with orchestration
- **Storage**: Hive-managed Spark tables in `analytics` schema
- **Access**:
  - Airflow UI at http://localhost:8080 (user: `airflow`, password: `airflow`)
  - dbt docs at http://localhost:8081
  - Metabase at http://localhost:3000

### Data Pipeline Flow (Airflow Environment)

The `generate_customer_marketing_metrics` DAG implements a complete ELT pipeline:

1. **Extract & Load** (`extract_data` task):
   - `generate_data.py`: Uses DuckDB to generate TPC-H data at scale factor 0.1, exports to CSV
   - `run_ddl.py`: Creates Spark/Hive tables in `analytics` schema and loads CSV data using PySpark

2. **Transform** (`dbt_run` task):
   - **Staging layer** (`models/staging/`): Clean source data with standardized naming
   - **Core layer** (`models/marts/core/`): Dimensional models (`dim_customer`) and denormalized fact tables (`wide_orders`, `wide_lineitem`)
   - **Marts layer** (`models/marts/sales/`): Business metrics (`customer_outreach_metrics`)

3. **Documentation** (`dbt_docs_gen` task): Generates dbt lineage and model documentation

4. **Visualization** (`generate_dashboard` task): Creates Plotly dashboard showing top customers by average order value

### dbt Project Structure

- **Source**: Raw tables in `analytics` schema defined in `models/staging/src.yml`
- **Profiles**: dbt uses Spark session method (not Thrift) configured in `tpch_analytics/profiles.yml`
- **Models**: Three-layer architecture (staging → core → marts)
- **Materialization**: Views by default (can be overridden per model)

## Common Commands

### Jupyter/Spark Environment

Start containers:
```bash
docker compose up -d
sleep 30
```

Stop containers:
```bash
docker compose down
```

Access Jupyter notebooks at http://localhost:8888/lab/tree/notebooks/starter-notebook.ipynb

### Airflow/dbt Environment

**Important**: Always run these commands from the `airflow/` directory.

Start Airflow (first time or after changes):
```bash
cd airflow
make restart  # Creates folders with correct permissions, builds and starts containers
```

Start Airflow (subsequent times):
```bash
cd airflow
make up
```

Stop Airflow:
```bash
make down
```

Access Airflow scheduler shell:
```bash
make sh
```

Serve dbt documentation (after running the DAG):
```bash
make dbt-docs
```

### Running dbt Manually

Inside the scheduler container (`make sh`):
```bash
cd /opt/airflow/tpch_analytics
dbt run --profiles-dir . --project-dir .
dbt test --profiles-dir . --project-dir .
dbt docs generate --profiles-dir . --project-dir .
```

### Data Generation

Generate TPC-H data with custom parameters:
```bash
python generate_data.py --sf 0.1 --format csv --output ./data
```

## Key Implementation Details

### Spark Configuration
- Both environments use PySpark with different metastore configurations
- Jupyter environment: Iceberg tables with REST catalog
- Airflow environment: Hive metastore with `enableHiveSupport()`

### dbt Models
- Use `{{ source('source', 'table_name') }}` to reference raw tables in staging
- Use `{{ ref('model_name') }}` for model-to-model references
- All models in `analytics` schema
- Profile uses `method: session` for direct Spark session access (not Thrift server)

### Data Flow Pattern
The pipeline follows ELT (Extract, Load, Transform):
1. Generate data with DuckDB (TPC-H dbgen)
2. Load raw data into Spark tables
3. Transform with dbt using SQL
4. Visualize results with Plotly/Metabase

### File Locations
- **Airflow DAGs**: `airflow/dags/`
- **Python scripts for data generation**: `airflow/containers/airflow/`
- **dbt project**: `airflow/tpch_analytics/`
- **Generated data**: `airflow/data/`
- **Visualizations**: `airflow/visualization/` or `airflow/tpch_analytics/dashboard_plot.html`
- **Jupyter notebooks**: `notebooks/`

## Environment Switching

**Critical**: You must stop one environment before starting the other, as they use overlapping ports (8080, 8888, 10000):

```bash
# From Jupyter to Airflow
docker compose down
cd airflow
make restart

# From Airflow to Jupyter
make down
cd ..
docker compose up -d
```
