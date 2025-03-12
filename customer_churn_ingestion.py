from pyspark.sql.functions import col, sha2,when
from pyspark.sql import SparkSession

spark = (SparkSession.builder.appName("CustomerChurnDataIngestion")
         .config("spark.jars","/opt/spark/jars/mysql-connector-j-8.0.33.jar")
         .getOrCreate())


def customer_data_load(db_configs,database_type,input_file):
    print("started job run...")
    db_url = db_configs[database_type]["url"]
    db_properties = db_configs[database_type]["properties"]
    print(f"input_file:={input_file}")

    chunk_size = 500
    mode = "overwrite"

    csv_reader = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(input_file)
    num_rows = csv_reader.count()
    print(f"num_rows:={num_rows}")
    chunk_no = 0;

    while True:
        print(f"started chunk no...{chunk_no}")
        df_chunk_data = csv_reader.limit(chunk_size)
        df_chunk_data.show(truncate=False)
        if df_chunk_data.isEmpty():
            break

        csv_reader = csv_reader.subtract(df_chunk_data)

        df_chunk_data = df_chunk_data.withColumn("CustomerID",
                                                 when(col("CustomerID").isNull() | (col("CustomerID") == ""),
                                                      "Unknown").otherwise(col("CustomerID")))

        df_chunk_data = df_chunk_data.withColumn("Age", when(col("Age").isNull() | (col("Age") == ""), 0).otherwise(
            col("Age")))

        if "CustomerID" in df_chunk_data.columns:
            df_chunk_data = df_chunk_data.withColumn("CustomerID", sha2(col("CustomerID").cast("string"), 256))

        if "Email" in df_chunk_data.columns:
            df_chunk_data = df_chunk_data.withColumn("Email", sha2(col("Email"), 256))

        df_chunk_data.write.jdbc(url=db_url, table="customer_churn_stage", mode=mode, properties=db_properties)
        chunk_no = chunk_no + 1

        print(f"Loaded data for chunk:= {chunk_no} with count:={df_chunk_data.count()}")
    print("Data Ingestion Completed!...")

db_configs = {
        "mysql": {
            "url": "jdbc:mysql://mysql:3306/customer_churn?allowPublicKeyRetrieval=true&useSSL=false",
            "properties": {"user": "etl_user", "password": "etl_user123", "driver": "com.mysql.cj.jdbc.Driver"}
        }
}
customer_data_load(db_configs,  "mysql", "/opt/data/customer_churn_data.csv")

spark.stop()




