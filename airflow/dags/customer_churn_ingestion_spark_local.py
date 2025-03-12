from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.bash import BashOperator


default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
    "retries": 0
}

JARS_PATH="/opt/spark/jars/mysql-connector-j-8.0.33.jar"
SPARK_HOME="/opt/bitnami/spark"
SPARK_SCRIPT="/opt/sparkjobs/customer_churn_ingestion_spark_local.py"

dag = DAG(
    "customer_churn_data_processing_spark_local",
    default_args=default_args,
    schedule_interval="@daily",
    catchup=False,
)

customer_churn_ingestion_task = BashOperator(
    task_id="run_customer_churn_ingestion",
    bash_command="spark-submit --conf spark.worker.timeout=30s --conf spark.worker.cleanup.enabled=true --name arrow-spark --conf spark.driver.extraClassPath=/opt/spark/jars/mysql-connector-j-8.0.33.jar --queue root.default /opt/sparkjobs/customer_churn_ingestion.py",
    dag=dag,
)

customer_churn_aggregation_task = BashOperator(
    task_id="run_customer_churn_aggregation",
    bash_command="spark-submit --conf spark.worker.timeout=30s --conf spark.worker.cleanup.enabled=true --name arrow-spark --conf spark.driver.extraClassPath=/opt/spark/jars/mysql-connector-j-8.0.33.jar --queue root.default /opt/sparkjobs/customer_churn_aggregation.py",
    dag=dag,
)

customer_churn_ingestion_task >> customer_churn_aggregation_task