import threading
import time
from threading import Semaphore
from django.db import models
from django.apps import apps
from django.conf import settings
from django.db import transaction
from django.core.management import call_command
from django.utils import timezone
import pandas as pd
import json
import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, when
from datetime import datetime
import os
from django.db.models import Q
from pathlib import Path
from django.conf import settings
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

MAX_THREADS = 5
semaphore = Semaphore(MAX_THREADS)

BASE_DIR = Path(__file__).resolve().parent.parent

def process_recon_request(reconvo_id):
    """
    Function to process a single ReconVO request.
    """
    try:
        # Acquire semaphore to ensure no more than MAX_THREADS run concurrently
        semaphore.acquire()

        # Dynamically load the model inside the function
        ReconVO = apps.get_model('NeuroReconUI', 'ReconVO')

        # Fetch the request based on ReconVO ID
        reconvo = ReconVO.objects.get(id=reconvo_id)

        if reconvo.field6 != 'Finished' and reconvo.batch == 'EOD':
            # Update status to 'Running' before processing
            reconvo.field6 = 'Running'
            reconvo.save()

            # Simulating some processing logic
            print(f"Processing request {reconvo.reqId}...")
            recon(reconvo)
            
            # After processing, update status to 'Finished'
            reconvo.field6 = 'Finished'
            reconvo.save()

            print(f"Finished processing request {reconvo.reqId}")
        
    finally:
        # Release the semaphore so another thread can run
        semaphore.release()

def monitor_and_process_requests():
    """
    Function that continuously monitors the ReconVO table for requests that need processing.
    """
    while True:
        # Dynamically load the model inside the function
        ReconVO = apps.get_model('NeuroReconUI', 'ReconVO')

        # Fetch the ReconVO requests that are InProgress and have EOD batch
        reconvos = ReconVO.objects.filter(~Q(field6="InProgress"), batch="EOD")

        if reconvos:
            for reconvo in reconvos:
                # Create a thread to process each request
                thread = threading.Thread(target=process_recon_request, args=(reconvo.id,))
                thread.start()

        # Sleep for a few seconds before checking the database again
        time.sleep(10)  # Adjust this based on how frequently you want to check

def start_monitoring():
    """
    Start the monitoring in a separate thread
    """
    monitoring_thread = threading.Thread(target=monitor_and_process_requests)
    monitoring_thread.daemon = True  # This makes the thread exit when the main program ends
    monitoring_thread.start()

# Start the monitoring when the application starts
start_monitoring()



# Function to fetch JSON from API
def fetch_json_from_api(url, payload):
    headers = {
        'Content-Type': 'application/json',
        
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(response.json())
        return response.json()
    else:
        raise Exception(f"Error fetching data from API. Status code: {response.status_code}")

def recon(reconvo):
    # Load the Excel file and sheet
    #excel_file = 'Staging\\DataModel\\OrderDataModel.xlsx'  # Path to your uploaded Excel file
    excel_file = os.path.join(BASE_DIR, 'Staging', 'DataModel', "OrderDataModel.xlsx")
    df = pd.read_excel(excel_file)

    # Extract the column names, mappings, and data types from the 'Destinationtype' column
    column_names = df['ColumnName'].tolist()  # Get all ColumnNames
    mappings = df['Mapping'].tolist()  # Get all Mappings
    data_types = df['Destinationtype'].tolist()  # Get all DataTypes from the 'Destinationtype' column

    # Load the JSON file (Product.json)
    json_file = os.path.join(BASE_DIR, 'Staging', 'Incoming', 'Order',"Order.json")
    with open(json_file, 'r') as f:
        json_data = json.load(f)

    # Initialize a list to store the final dataset
    final_dataset = []


    # Function to map the data type string to PySpark data types
    def get_spark_data_type(data_type):
        if data_type == 'Integer':
            return IntegerType()
        elif data_type == 'Float':
            return FloatType()
        elif data_type == 'String':
            return StringType()
        else:
            return StringType()  # Default to StringType if not found


    # Dynamically create the schema using 'Destinationtype' for each column
    schema_fields = []
    for col_name, data_type in zip(column_names, data_types):
        spark_data_type = get_spark_data_type(data_type)
        schema_fields.append(StructField(col_name, spark_data_type, True))  # Add each field to the schema

    # Define the schema
    schema = StructType(schema_fields)


    # Function to extract values using XPath (simulated using dot notation)
    def get_value_from_json(data, xpath):
        keys = xpath.split('.')  # Split the XPath into individual keys
        temp = data
        for key in keys:
            if isinstance(temp, dict) and key in temp:
                temp = temp[key]  # Navigate through the JSON dictionary
            else:
                print(f"Missing path: {xpath}")  # Debugging line to track missing paths
                return None  # Return None if path doesn't exist
        return temp


    # Iterate through the JSON data and map using the mappings and column names
    for record in json_data['results']:  # Assuming your JSON is in a 'results' array
        mapped_record = {}  # Initialize a dictionary for each record

        for col_name, mapping in zip(column_names, mappings):
            value = get_value_from_json(record, mapping)  # Get value from JSON based on XPath
            mapped_record[col_name] = value  # Map it to the column name

        final_dataset.append(mapped_record)

    # Output the final dataset (show it nicely formatted)
    final_output = json.dumps(final_dataset, indent=4)
    print(final_output)


    # Initialize Spark session

    jarf = os.path.join(BASE_DIR, 'Jars', 'postgresql-42.7.5.jar')
    
    spark = SparkSession.builder.appName('JsonComparison').master('local[*]').config("spark.jars",jarf).enableHiveSupport().getOrCreate()

    # Convert the final dataset (list of dictionaries) to Spark DataFrame using the defined schema
    final_spark_df = spark.createDataFrame(final_dataset, schema)

    env = 'LOCAL'
    #settings.ENV

    if env == 'LOCAL':
        base_url = "http://localhost:8000"
        print("In Local Environment")
    else:
        base_url = "http://13.48.57.113:8000"
        print("In Development Environment")


    # Define API URLs
    url_json1 = f"{base_url}/get_kafka_data/"
    url_json2 = f"{base_url}/get_impala_data/"
    url_json3 = f"{base_url}/get_gemfire_data/"

    payload = {
        "key": "value"
    }

    # Fetch JSON data from APIs
    json1_data = fetch_json_from_api(url_json1, payload)
    json2_data = fetch_json_from_api(url_json2, payload)
    json3_data = fetch_json_from_api(url_json3, payload)

    spark.sparkContext.setLogLevel("ERROR")

    # Read the JSON data into Spark DataFrames
    df1 = spark.read.json(spark.sparkContext.parallelize([json1_data]))
    df2 = spark.read.json(spark.sparkContext.parallelize([json2_data]))
    df3 = spark.read.json(spark.sparkContext.parallelize([json3_data]))

    # Step 4: Generate a dummy Request ID
    request_id = f"req{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Step 5: Compare field by field and prepare recon output
    cdc_columns_df = df[df['CDC'] == 'Y']
    fields = cdc_columns_df['ColumnName'].tolist()

    nk_columns_df = df[df['NaturalKey'] == 'Y']
    joinKey = nk_columns_df['ColumnName'].tolist()[0]

    # Step 3: Join on the key (SMCP)
    joined = final_spark_df.alias("df1") \
        .join(df2.alias("df2"), on=joinKey, how="outer") \
        .join(df3.alias("df3"), on=joinKey, how="outer")

    recon_data = []

    # Perform column-wise comparison for CDC fields
    for field in fields:
        recon_data.append(
            joined.select(
                col(joinKey).alias("JoinKey"),  # JoinKey FIRST
                lit(field).alias("FieldName"),
                col(f"df1.{field}").alias("Kafka"),
                col(f"df2.{field}").alias("Impala"),
                col(f"df3.{field}").alias("Gemfire"),
                when(
                    (col(f"df1.{field}") == col(f"df2.{field}")) &
                    (col(f"df2.{field}") == col(f"df3.{field}")),
                    "Match"
                ).otherwise("Mismatch").alias("ReconStatus"),
                lit(reconvo.reqId).alias("RequestID")
            )
        )

    # Step 6: Union all comparisons
    final_df = recon_data[0]
    for df in recon_data[1:]:
        final_df = final_df.union(df)

    # Step 7: Show output
    final_df.show(truncate=False)
    final_df = final_df.withColumn("env", lit("prod"))

    # # Step 8: Write the results to a PostgreSQL database
    DATABASE_NAME = settings.DATABASES['default']['NAME']  # 'NAME' is the database name
    DATABASE_USER = settings.DATABASES['default']['USER']  # 'USER' is the username
    DATABASE_PASSWORD = settings.DATABASES['default']['PASSWORD']  # 'PASSWORD' is the password
    DATABASE_HOST = settings.DATABASES['default']['HOST']  # 'HOST' is the host, e.g., 'localhost'

    # Define JDBC URL for PostgreSQL
    #jdbc_url = f"jdbc:postgresql://{DATABASE_HOST}:5432/{DATABASE_NAME}"
    #jdbc_url = "jdbc:postgresql://localhost:5432/telusko"
    # Write the DataFrame to PostgreSQL
    jdbc_url = f"jdbc:postgresql://{DATABASE_HOST}:5432/{DATABASE_NAME}"

    final_df.write \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", "neuroreconui_reconresult") \
        .option("user", DATABASE_USER) \
        .option("password", DATABASE_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()
    print('Data Written')

    if(reconvo.temporal =='TYPE2'):
        print('Process History')
    #     final_spark_df
    #     from pyspark.sql import SparkSession
    #     from pyspark.sql.functions import explode, array, col, expr, md5, concat_ws
    #     cdcfile = os.path.join(BASE_DIR, 'Staging', '\DataModel', "ProductCDC.json")
    #     df = spark.read.format("json").option("multiline", True).load(cdcfile)
    #     df.printSchema()
    #     df = df.select(explode(array(col("ProductCDC.cdc"))).alias("productcdc"))
    #     cdc_df = df.select(explode(col("productcdc")).alias("cdc"))
    #     fields = [row['cdc'] for row in cdc_df.collect()]
    #     stv = "concat_ws(''," + ",".join([f"nvl(cast({field} as string), '^A')" for field in fields]) + ")"
    #     result_df = final_spark_df.withColumn("md5_hash_key", md5(expr(stv)))
    #     from pyspark.sql.functions import col, when
    #     same_record_condition = (
    #     col("active.OrderId").eqNullSafe(col("delta.OrderId")) &
    #     col("active.md5_hash_key").eqNullSafe(col("delta.md5_hash_key")))
    #     full = (
    #     result_df.alias("active")  #this needs to be changed
    #    .join(result_df.alias("delta"), col("active.OrderId").eqNullSafe(col("delta.OrderId")), "full_outer")
    #    .withColumn(
    #     "action",
    #     when(col("delta.OrderId").isNotNull() & col("active.OrderId").isNull(), "insert")
    #     .when(col("delta.OrderId").isNull() & col("active.OrderId").isNotNull(), "discard")
    #     .when(same_record_condition, "history")
    #     .otherwise("update")
    #         )
    #     )
    #     update_records_old = full.select("active.*").where(col("action") == "update")
    #     df2 #current history for new record
    #     joined = update_records_old.alias("df1").join(df2.alias("df2"), on=joinKey, how="outer")

    #     recon_data = []

    #     for field in fields:
    #         recon_data.append(
    #             joined.select(
    #                 col(joinKey).alias("JoinKey"),  # JoinKey FIRST
    #                 lit(field).alias("FieldName"),
    #                 col(f"df1.{field}").alias("ExpectedHist"),
    #                 col(f"df2.{field}").alias("ActualHist"),
    #                 when((col(f"df1.{field}") == col(f"df2.{field}"))), "Match" ).otherwise("Mismatch").alias("ReconStatus"),
    #                 lit(reconvo.reqId).alias("RequestID")
    #             )
    #     final_df = recon_data[0]
    #     for df in recon_data[1:]:
    #         final_df = final_df.union(df)
    #         final_df.show()        
