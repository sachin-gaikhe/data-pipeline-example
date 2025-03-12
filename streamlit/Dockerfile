FROM python:3.9

# Install Java 17 (Required for PySpark)
RUN apt-get update && apt-get install -y openjdk-17-jdk

# Ensure Java is installed in the correct location
RUN update-alternatives --config java

# Set Java Home Environment Variable
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64/bin
ENV PATH=$JAVA_HOME/bin:$PATH

# Set working directory
WORKDIR /app

# Copy the Streamlit app files into the container
COPY customer_churn_visualization.py /app

# Install dependencies
RUN pip install --no-cache-dir \
    streamlit \
    pandas \
    pymysql \
    pyspark \
    matplotlib

# Expose Streamlit port
EXPOSE 8501

CMD ["streamlit", "run", "customer_churn_visualization.py", "--server.port=8501", "--server.address=0.0.0.0"]