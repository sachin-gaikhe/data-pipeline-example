
from pyspark.sql.functions import col, sha2, count, when, avg, sum, stddev,min,max,when
from pyspark.sql import SparkSession
from pyspark.sql.functions import when


spark = (SparkSession.builder.appName("CustomerChurnDataAggregation")
         .config("spark.jars","/opt/spark/jars/mysql-connector-j-8.0.33.jar")
         .getOrCreate())


def customer_data_aggragations(db_configs,database_type):
    db_url = db_configs[database_type]["url"]
    db_properties = db_configs[database_type]["properties"]

    customer_df = spark.read.jdbc(url=db_url, table="customer_churn_stage", properties=db_properties)

    customer_df = customer_df.withColumn("TotalCharges", col("TotalCharges").cast("double"))
    customer_df = customer_df.withColumn("MonthlyCharges", col("MonthlyCharges").cast("double"))
    customer_df = customer_df.withColumn("Tenure", col("Tenure").cast("int"))
    customer_df = customer_df.withColumn("Age", col("Age").cast("int"))

    churn_report = customer_df.groupBy("Churn").agg(
        count("CustomerID").alias("Total_Customers"),
        avg("Tenure").alias("Avg_Tenure"),
        avg("MonthlyCharges").alias("Avg_MonthlyCharges"),
        sum("TotalCharges").alias("Total_Revenue")
    )
    churn_report.write.jdbc(url=db_url, table="churn_aggregates", mode="overwrite", properties=db_properties)

    contract_report = customer_df.groupBy("ContractType").agg(
        count("CustomerID").alias("Total_Customers"),
        avg("Tenure").alias("Avg_Tenure"),
        sum("TotalCharges").alias("Total_Revenue")
    )
    contract_report.write.jdbc(url=db_url, table="contract_type_aggregates", mode="overwrite",
                               properties=db_properties)

    internet_report = customer_df.groupBy("InternetService").agg(
        count("CustomerID").alias("Total_Customers"),
        avg("MonthlyCharges").alias("Avg_MonthlyCharges"),
        sum("TotalCharges").alias("Total_Revenue")
    )
    internet_report.write.jdbc(url=db_url, table="internet_service_aggregates", mode="overwrite",
                               properties=db_properties)

    tech_support_report = customer_df.groupBy("TechSupport").agg(
        count("CustomerID").alias("Total_Customers"),
        avg("Tenure").alias("Avg_Tenure"),
        sum("TotalCharges").alias("Total_Revenue")
    )
    tech_support_report.write.jdbc(url=db_url, table="tech_support_aggregates", mode="overwrite",
                                   properties=db_properties)

    gender_report = customer_df.groupBy("Gender").agg(
        count("CustomerID").alias("Total_Customers"),
        avg("Age").alias("Avg_Age"),
        avg("Tenure").alias("Avg_Tenure"),
        sum("TotalCharges").alias("Total_Revenue")
    )
    gender_report.write.jdbc(url=db_url, table="gender_aggregates", mode="overwrite", properties=db_properties)

    customer_df = customer_df.withColumn("Tenure_Bucket", when(col("Tenure") < 12, "0-12 months")
                                         .when(col("Tenure") < 24, "12-24 months")
                                         .when(col("Tenure") < 48, "24-48 months")
                                         .otherwise("48+ months"))
    tenure_churn_report = customer_df.groupBy("Tenure_Bucket", "Churn").agg(
        count("CustomerID").alias("Total_Customers"),
        avg("MonthlyCharges").alias("Avg_MonthlyCharges"),
        sum("TotalCharges").alias("Total_Revenue")
    )
    tenure_churn_report.write.jdbc(url=db_url, table="tenure_churn_aggregates", mode="overwrite",
                                   properties=db_properties)

    print("All reports have been successfully generated and stored in MySQL.")

    spark.stop()

db_configs = {
        "mysql": {
            "url": "jdbc:mysql://mysql:3306/customer_churn?allowPublicKeyRetrieval=true&useSSL=false",
            "properties": {"user": "etl_user", "password": "etl_user123", "driver": "com.mysql.cj.jdbc.Driver"}
        }
    }

customer_data_aggragations(db_configs,"mysql")

spark.stop()




