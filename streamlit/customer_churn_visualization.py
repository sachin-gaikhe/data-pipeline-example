import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pyspark.sql import SparkSession

# Initialize Spark Session
spark = (SparkSession.builder.appName("CustomerChurnStreamlit")
         .config("spark.jars", "/opt/spark/jars/mysql-connector-j-8.0.33.jar")
         .getOrCreate())

# Database Connection Configurations
db_url = "jdbc:mysql://mysql:3306/customer_churn?allowPublicKeyRetrieval=true&useSSL=false"
db_properties = {"user": "etl_user", "password": "etl_user123", "driver": "com.mysql.cj.jdbc.Driver"}

data = spark.read.jdbc(url=db_url, table="churn_aggregates", properties=db_properties)
df = data.toPandas()

# Display the dataframe
st.subheader("📋 Customer Churn Summary")
st.dataframe(df.style.format({"Avg_Tenure": "{:.2f}", "Avg_MonthlyCharges": "{:.2f}", "Total_Revenue": "{:,.2f}"}))

# Create a bar chart for Average Tenure and Monthly Charges
st.subheader("📉 Comparison of Average Tenure and Monthly Charges")

fig, ax = plt.subplots(figsize=(8, 5))
df.set_index("Churn")[["Avg_Tenure", "Avg_MonthlyCharges"]].plot(kind="bar", ax=ax, color=["blue", "orange"])
ax.set_ylabel("Value")
ax.set_title("Avg Tenure vs Avg Monthly Charges by Churn Status")
st.pyplot(fig)

# Create a bar chart for Total Revenue
st.subheader("💰 Total Revenue by Churn Status")

fig, ax = plt.subplots(figsize=(8, 5))
df.set_index("Churn")["Total_Revenue"].plot(kind="bar", ax=ax, color=["green", "red"])
ax.set_ylabel("Total Revenue ($)")
ax.set_title("Total Revenue by Churn Status")
st.pyplot(fig)

#### We can add more reports here ###