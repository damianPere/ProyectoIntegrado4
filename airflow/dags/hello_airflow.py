from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta

# Definir argumentos por defecto del DAG
default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2024, 3, 18),  # Cambia la fecha si es necesario
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

# Definir el DAG
with DAG(
    "mi_primer_dag",
    default_args=default_args,
    description="Un DAG de prueba con Airflow",
    schedule_interval=timedelta(days=1),
    catchup=False,
) as dag:

    # Tarea de inicio
    tarea_inicio = EmptyOperator(task_id="inicio")

    # Tarea final
    tarea_final = EmptyOperator(task_id="fin")

    # Definir el flujo de trabajo

    tarea_inicio >> tarea_final
