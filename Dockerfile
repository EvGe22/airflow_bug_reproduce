FROM apache/airflow:2.2.3
USER root
COPY dags /opt/airflow/dags
COPY airflow.cfg /opt/airflow/airflow.cfg
