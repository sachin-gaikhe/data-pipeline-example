from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "retries": 0
}

JARS_PATH="/opt/spark/jars/mysql-connector-j-8.0.33.jar"

dag = DAG(
    "customer_churn_data_processing_spark_cluster",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
)

customer_churn_ingestion_task = SparkSubmitOperator(
    task_id='run_customer_churn_ingestion_spark_job',
    application='/opt/sparkjobs/customer_churn_ingestion.py',
    conn_id='spark_config',
    verbose=True,
    application_args=[],
    conf={
        "spark.executor.instances": "2",
        "spark.executor.cores": "2",
        "spark.executor.memory": "2G",
        "spark.driver.extraClassPath": JARS_PATH,
        "spark.executor.extraClassPath": JARS_PATH
},
    dag=dag,
)

customer_churn_aggregation_task = SparkSubmitOperator(
    task_id='run_customer_churn_aggregation_spark_job',
    application='/opt/sparkjobs/customer_churn_aggregation.py',
    conn_id='spark_config',
    verbose=True,
    application_args=[],
    conf={
            "spark.executor.instances": "2",
            "spark.executor.cores": "2",
            "spark.executor.memory": "2G",
            "spark.driver.extraClassPath": JARS_PATH,
            "spark.executor.extraClassPath": JARS_PATH
        },
    dag=dag,
)

customer_churn_ingestion_task >> customer_churn_aggregation_task