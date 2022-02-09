from datetime import datetime
from airflow import DAG
from common import get_end_task, get_start_task, heavy_computation_task, create_group

DAG_ID = "Manual_Quick_DAG"
SCHEDULE_INTERVAL = None
GROUPS_N = 2
GROUP_MEMBERS_N = 5
args = {
    'owner': 'airflow',
    'start_date': datetime.now(),
}

main_dag = DAG(
    DAG_ID,
    schedule_interval=SCHEDULE_INTERVAL,
    default_args=args,
    is_paused_upon_creation=False,
    max_active_tasks=2
)

start = get_start_task(main_dag)
end = get_end_task(main_dag)
create_group(n_tasks=GROUPS_N, n_subtasks=GROUP_MEMBERS_N, task_callable=heavy_computation_task,
             dag=main_dag, start_task=start, end_task=end)
