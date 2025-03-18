from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# Definir argumentos por defecto
default_args = {
    "owner": "airflow",
    "start_date": datetime(2025, 3, 17),  # Fecha de inicio del DAG
    "retries": 1,
}

# Crear el DAG
with DAG(
    dag_id="etl_proyecto",
    default_args=default_args,
    schedule_interval="@daily",  # Corre todos los días
    catchup=False,
) as dag:

    # Tarea 1: Extraer datos
    extract_task = BashOperator(
        task_id="extract",
        bash_command="cd /opt/airflow/proyecto_integrador && python src/extract.py",
    )
    # Tarea 2: Cargar datos
    load_task = BashOperator(
        task_id="load",
        bash_command="cd /opt/airflow/proyecto_integrador && python src/load.py",
    )
    # Tarea 3: Transformar datos
    transform_task = BashOperator(
        task_id="transform",
        bash_command="cd /opt/airflow/proyecto_integrador && python src/transform.py",
    )

    # Definir el orden de ejecución
    extract_task >> load_task >> transform_task
