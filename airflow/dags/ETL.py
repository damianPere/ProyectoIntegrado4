from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Definir argumentos por defecto
default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 4, 1),
    "retries": 1,
    "retry_delay": timedelta(minutes=2),
}

# Crear el DAG
with DAG(
    dag_id="etl_proyecto",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
) as dag:

    def run_extract():
        import sys

        sys.path.append("/opt/airflow/proyecto_integrador")
        from src.extract import extract
        from src import config

        csv_folder = config.DATASET_ROOT_PATH
        public_holidays_url = config.PUBLIC_HOLIDAYS_URL
        csv_table_mapping = config.get_csv_to_table_mapping()
        return extract(csv_folder, csv_table_mapping, public_holidays_url)

    def run_load(ti):
        import sys

        sys.path.append("/opt/airflow/proyecto_integrador")
        from src.load import load
        from src import config
        from sqlalchemy import create_engine
        from pathlib import Path

        # Obtener datos de la tarea anterior
        csv_dataframes = ti.xcom_pull(task_ids="extract_task")

        # Configurar base de datos
        Path(config.SQLITE_BD_ABSOLUTE_PATH).touch()
        ENGINE = create_engine(
            rf"sqlite:///{config.SQLITE_BD_ABSOLUTE_PATH}", echo=False
        )

        # Cargar datos
        load(data_frames=csv_dataframes, database=ENGINE)

    extract_task = PythonOperator(
        task_id="extract_task",
        python_callable=run_extract,
    )

    load_task = PythonOperator(
        task_id="load_task",
        python_callable=run_load,
    )

    # Para la tarea de transformación puedes usar un BashOperator o un PythonOperator
    transform_task = BashOperator(
        task_id="transform_task",
        bash_command="cd /opt/airflow/proyecto_integrador && python src/transform.py",
    )

    # Definir el orden de ejecución para el flujo ELT
    extract_task >> load_task >> transform_task
