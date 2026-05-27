from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'flight-pulse',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# DAG
with DAG(
    dag_id='flight_pipeline',
    default_args=default_args,
    description='Performs dbt transformation every hour',
    schedule=timedelta(hours=1),
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=['flight-pulse', 'dbt'],
) as dag:
    dbt_staging = BashOperator(
        task_id='dbt_staging',
        bash_command='docker exec dbt dbt run --select staging',
    )

    dbt_intermediate = BashOperator(
        task_id='dbt_intermediate',
        bash_command='docker exec dbt dbt run --select intermediate',
    )

    dbt_marts = BashOperator(
        task_id='dbt_marts',
        bash_command='docker exec dbt dbt run --select marts',
    )
    
dbt_staging >> dbt_intermediate >> dbt_marts