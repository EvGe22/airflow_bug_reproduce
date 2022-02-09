import random
from time import sleep

from airflow.operators.python import PythonOperator
from airflow.models import BaseOperator
import logging
from airflow import DAG
from airflow.utils.task_group import TaskGroup
from typing import Callable, Any


def get_start_task(dag: DAG) -> BaseOperator:
    return PythonOperator(
        task_id='start',
        dag=dag,
        python_callable=lambda : logging.info(f"Starting {dag.dag_id}"))


def get_end_task(dag: DAG) -> BaseOperator:
    return PythonOperator(
        task_id='end',
        dag=dag,
        python_callable=lambda: logging.info(f"Ending {dag.dag_id}"))


def heavy_computation_task() -> int:
    sleep(random.randint(250, 900))
    return random.randint(100, 300) + random.randint(100, 300)


def light_computation_task() -> int:
    sleep(random.randint(10, 100))
    return random.randint(10, 100) + random.randint(10, 100)


def create_group(
    n_tasks: int,
    n_subtasks: int,
    task_callable: Callable[[], Any],
    dag: DAG,
    start_task: BaseOperator,
    end_task: BaseOperator
) -> None:
    with TaskGroup(group_id="files_processing", dag=dag) as main_tg:
        for group_i in range(n_tasks):
            with TaskGroup(group_id=f"group_{group_i}", dag=dag, parent_group=main_tg) as secondary_tg:
                subcommands = [f"command_{i}" for i in range(n_subtasks)]
                first_command = subcommands.pop(0)
                first_task = PythonOperator(
                    task_id=first_command,
                    dag=dag,
                    python_callable=task_callable
                )

                for subcommand in subcommands:
                    second_task = PythonOperator(
                        task_id=subcommand,
                        dag=dag,
                        python_callable=task_callable
                    )
                    first_task >> second_task
                    first_task = second_task

        start_task >> main_tg >> end_task

