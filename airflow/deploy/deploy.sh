#!/bin/bash

ENV=$1  # Accepts "dev", "qa", "prod"
DAG_BUCKET=""

case "$ENV" in
  dev) DAG_BUCKET="s3://dev-airflow-dags/" ;;
  qa) DAG_BUCKET="s3://qa-airflow-dags/" ;;
  prod) DAG_BUCKET="s3://prod-airflow-dags/" ;;
  *) echo "Invalid environment"; exit 1 ;;
esac

echo "Deploying DAGs to $DAG_BUCKET ..."
aws s3 sync dags/ $DAG_BUCKET

echo "Restarting Airflow Scheduler..."
kubectl rollout restart deployment airflow-scheduler -n airflow

#### Usage
#bash deploy.sh dev  # Deploy DAGs to Dev
#bash deploy.sh qa   # Deploy DAGs to QA
#bash deploy.sh prod # Deploy DAGs to Prod
