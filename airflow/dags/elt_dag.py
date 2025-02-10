from datetime import datetime
from airflow import DAG
from docker.types import Mount

from airflow.operators.python_operator import PythonOperator
from airflow.providers.docker.operators.docker import DockerOperator

import subprocess

#from airflow.exceptions import AirflowException
#import logging
from airflow.operators.dummy_operator import DummyOperator


default_args = {
    'owner': 'airflow',
#    'retries': 3,
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False
}

def run_elt_script():
    script_path = "/opt/airflow/elt/elt_script.py"
    result = subprocess.run(["python", script_path],
                            capture_output=True,
                            text=True)
    if result.returncode != 0:
        raise Exception(f"Script failed with error: {result.stderr}")
    else:
        print(result.stdout)
# prints error description in case task marked as failure
def task_failure(context):
    print(f"Task has failed, task_instance_key_str: {context['task_instance_key_str']}")

with DAG(
    'elt_and_dbt',
    default_args=default_args,
    description='An ELT workflow with dbt',
    start_date=datetime(2025,2,6),
    catchup=False,
    on_failure_callback=task_failure,
):
# tasks for testing, marking beginning and ending of our dag 
    start_dag = DummyOperator(task_id="start_dag")
    end_dag = DummyOperator(task_id="end_dag")
# runs script
    task1 = PythonOperator(
        task_id="run_elt_script",
        python_callable=run_elt_script,
    ),
# connects with dbt    
    task2 = DockerOperator(
        task_id="dbt_run",
        image='ghcr.io/dbt-labs/dbt-postgres:1.4.7',
        # force_pull=True,
        command=[
            "run",
            "--profiles-dir",
            "/root",
            "--project-dir",
            "/dbt",
            "--full-refresh"
        ],
        auto_remove=True,
        docker_url="unix://var/run/docker.sock",
        network_mode="bridge",
        mounts=[
            Mount(
                source='/c/Users/User/elt/custom_postgres',
                target='/dbt',
                type='bind'
            ),
            Mount(
                source='/c/Users/User/.dbt',
                target='/root',
                type='bind'
            )
        ]
    )

    # order of tasks
    start_dag >> task1
    task1 >> task2
    task2 >> end_dag

