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
from django.db import transaction
import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, when
from datetime import datetime
import os
from django.db.models import Q
from pathlib import Path
from django.conf import settings
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

MAX_THREADS = 1
semaphore = Semaphore(MAX_THREADS)
BASE_DIR = Path(__file__).resolve().parent.parent

def process_recon_request(reconvo_id):
    try:
        semaphore.acquire()
        ReconVO = apps.get_model('NeuroReconUI', 'ReconVO')

        with transaction.atomic():
            reconvo = ReconVO.objects.select_for_update().get(id=reconvo_id)

            if reconvo.field6 != 'Finished' and reconvo.batch == 'EOD':
                reconvo.field6 = 'Running'
                reconvo.save()

        
        print(f"Started request {reconvo.reqId}")
        # Call recon outside the lock to keep lock duration short
        recon(reconvo)

        with transaction.atomic():
            reconvo = ReconVO.objects.get(id=reconvo_id)
            reconvo.field6 = 'Finished'
            reconvo.save()

        print(f"Finished processing request {reconvo.reqId}")
    
    finally:
        semaphore.release()

def monitor_and_process_requests():
    while True:
        ReconVO = apps.get_model('NeuroReconUI', 'ReconVO')
        reconvos = ReconVO.objects.filter(~Q(field6="Finished"), batch="EOD")
        if reconvos:
            for reconvo in reconvos:
                thread = threading.Thread(target=process_recon_request, args=(reconvo.id,))
                thread.start()

        time.sleep(1)  

def start_monitoring():
    monitoring_thread = threading.Thread(target=monitor_and_process_requests)
    monitoring_thread.daemon = True  # This makes the thread exit when the main program ends
    monitoring_thread.start()

start_monitoring()

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
    excel_file = os.path.join(BASE_DIR, 'Staging', 'DataModel', "OrderDataModel.xlsx")
    df = pd.read_excel(excel_file)
    column_names = df['ColumnName'].tolist()  
    mappings = df['Mapping'].tolist() 
    data_types = df['Destinationtype'].tolist() 

    json_file = os.path.join(BASE_DIR, 'Staging', 'Incoming', 'Order',"Order.json")
    with open(json_file, 'r') as f:
        json_data = json.load(f)

    final_dataset = []

    def get_spark_data_type(data_type):
        if data_type == 'Integer':
            return IntegerType()
        elif data_type == 'Float':
            return FloatType()
        elif data_type == 'String':
            return StringType()
        else:
            return StringType() 

    schema_fields = []
    for col_name, data_type in zip(column_names, data_types):
        spark_data_type = get_spark_data_type(data_type)
        schema_fields.append(StructField(col_name, spark_data_type, True)) 

    schema = StructType(schema_fields)

    def get_value_from_json(data, xpath):
        keys = xpath.split('.') 
        temp = data
        for key in keys:
            if isinstance(temp, dict) and key in temp:
                temp = temp[key]  
            else:
                print(f"Missing path: {xpath}") 
                return None  
        return temp


    for record in json_data['results']: 
        mapped_record = {} 

        for col_name, mapping in zip(column_names, mappings):
            value = get_value_from_json(record, mapping)  
            mapped_record[col_name] = value  

        final_dataset.append(mapped_record)

    final_output = json.dumps(final_dataset, indent=4)
    print(final_output)

    jarf = os.path.join(BASE_DIR, 'Jars', 'postgresql-42.7.5.jar')
    spark = SparkSession.builder.appName('JsonComparison').master('local[*]').config("spark.jars",jarf).enableHiveSupport().getOrCreate()
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
   
   
   
    url_json1 = f"{base_url}/get_kafka_data/"
    url_json2 = f"{base_url}/get_impala_data/"
    url_json3 = f"{base_url}/get_gemfire_data/"

    payload = {
        "key": "value"
    }

    #json1_data = fetch_json_from_api(url_json1, payload)
    json2_data = fetch_json_from_api(url_json2, payload)
    json3_data = fetch_json_from_api(url_json3, payload)
    spark.sparkContext.setLogLevel("ERROR")

    #df1 = spark.read.json(spark.sparkContext.parallelize([json1_data]))
    df2 = spark.read.json(spark.sparkContext.parallelize([json2_data]))
    df3 = spark.read.json(spark.sparkContext.parallelize([json3_data]))

    request_id = f"req{datetime.now().strftime('%Y%m%d%H%M%S')}"
    cdc_columns_df = df[df['CDC'] == 'Y']
    fields = cdc_columns_df['ColumnName'].tolist()
    nk_columns_df = df[df['NaturalKey'] == 'Y']
    joinKey = nk_columns_df['ColumnName'].tolist()[0]

    joined = final_spark_df.alias("df1") \
        .join(df2.alias("df2"), on=joinKey, how="outer") \
        .join(df3.alias("df3"), on=joinKey, how="outer")

    recon_data = []

    for field in fields:
        recon_data.append(
            joined.select(
                col(joinKey).alias("JoinKey"),lit(field).alias("FieldName"),
                col(f"df1.{field}").alias("Kafka"),
                col(f"df2.{field}").alias("Impala"),
                col(f"df3.{field}").alias("Gemfire"),
                when((col(f"df1.{field}") == col(f"df2.{field}")) & (col(f"df2.{field}") == col(f"df3.{field}")),"Match")
                .otherwise("Mismatch").alias("ReconStatus"),
                lit(reconvo.reqId).alias("RequestID")
            )
        )

    final_df = recon_data[0]
    print('1')
    final_df.show()
    for df in recon_data[1:]:
        final_df = final_df.union(df)

        print('2')
        final_df.show(truncate=False)
        final_df = final_df.withColumn("env", lit("Prod"))

    DATABASE_NAME = settings.DATABASES['default']['NAME']  
    DATABASE_USER = settings.DATABASES['default']['USER']  
    DATABASE_PASSWORD = settings.DATABASES['default']['PASSWORD'] 
    DATABASE_HOST = settings.DATABASES['default']['HOST'] 
    jdbc_url = f"jdbc:postgresql://{DATABASE_HOST}:5432/{DATABASE_NAME}"
    final_df.write \
        .format("jdbc") \
        .option("url", jdbc_url) \
        .option("dbtable", "NEURORECONUI_RECONRESULT") \
        .option("user", DATABASE_USER) \
        .option("password", DATABASE_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .mode("append") \
        .save()
    print('Data Written')