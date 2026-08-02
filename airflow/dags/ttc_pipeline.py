from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
from pathlib import Path

# Let Python find our scripts folder from inside the Airflow container
SCRIPTS_DIR = Path("/opt/airflow/scripts")
sys.path.append(str(SCRIPTS_DIR))

def run_load():
    import load_data

def run_clean():
    import clean_data

def run_upload():
    import upload_to_storage

with DAG(
    dag_id="ttc_transit_pipeline",
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
) as dag:

    load_task = PythonOperator(
        task_id="load_data",
        python_callable=run_load,
    )

    clean_task = PythonOperator(
        task_id="clean_data",
        python_callable=run_clean,
    )

    upload_task = PythonOperator(
        task_id="upload_to_storage",
        python_callable=run_upload,
    )

    load_task >> clean_task >> upload_task