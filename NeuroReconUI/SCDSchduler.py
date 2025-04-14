import threading
import time
from django.db.models import Q
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
from pathlib import Path
from django.conf import settings
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType
from NeuroReconUI.models import SCDVO

# Max threads allowed
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
        SCDVO = apps.get_model('NeuroReconUI', 'SCDVO')

        # Fetch the request based on ReconVO ID
        reconvo = SCDVO.objects.get(id=reconvo_id)

        if reconvo.status != 'Finished':
            # Update status to 'Running' before processing
            reconvo.status = 'Running'
            reconvo.save()

            # Simulating some processing logic
            print(f"Processing request {reconvo.reqId}...")
            excel_file = os.path.join(BASE_DIR, 'Staging', 'DataModel', 'OrderDataModel.xlsx')
            path=update_json_by_excel(reconvo.filePath,excel_file,reconvo.reqId)
            
            # After processing, update status to 'Finished'
            reconvo.outputFile=path
            reconvo.status = 'Finished'
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
        SCDVO = apps.get_model('NeuroReconUI', 'SCDVO')

        # Fetch the ReconVO requests that are InProgress and have EOD batch
        reconvos = SCDVO.objects.filter(~Q(status="Finished"))

        if reconvos:
            for reconvo in reconvos:
                # Create a thread to process each request
                thread = threading.Thread(target=process_recon_request, args=(reconvo.id,))
                thread.start()

        # Sleep for a few seconds before checking the database again
        time.sleep(10)  # Adjust this based on how frequently you want to check

# Start the monitoring when the application starts
def start_scdmonitoring():
    """
    Start the monitoring in a separate thread
    """
    monitoring_thread = threading.Thread(target=monitor_and_process_requests)
    monitoring_thread.daemon = True  # This makes the thread exit when the main program ends
    monitoring_thread.start()

# Start the monitoring when the application starts
start_scdmonitoring()
























def update_json_by_excel(json_path, excel_path, reqId,output_path=None):
    # Safety check for file existence
    if not os.path.exists(json_path):
        raise FileNotFoundError(f"JSON file not found: {json_path}")
    if not os.path.exists(excel_path):
        raise FileNotFoundError(f"Excel file not found: {excel_path}")

    # Set output file name if not provided
    if output_path is None:
        dir_name, file_name = os.path.split(json_path)
        name, ext = os.path.splitext(file_name)
        output_file_name = f"{name}SCD2{ext}"
        output_path = os.path.join(dir_name, output_file_name)

    # Load Excel and clean 'CDC' column
    df = pd.read_excel(excel_path)
    df['CDC'] = df['CDC'].astype(str).str.strip().str.upper()
    df = df[df['CDC'] == 'Y']
    df = df.dropna(subset=['Mapping'])

    # Get list of mappings like "Xref.OrderId"
    mappings = df['Mapping'].dropna().astype(str).str.strip().tolist()

    # Load JSON
    with open(json_path, 'r') as f:
        data = json.load(f)

        print("🔍 Extracting NaturalKey mappings...")
        mappings = get_natural_key_mappings(excel_path)
        order_ids = extract_order_ids_from_json_dynamic(json_path, mappings)

        jarf = os.path.join(BASE_DIR, 'Jars', 'postgresql-42.7.5.jar')
    
        print("🚀 Starting Spark session for filtering...")
        spark = SparkSession.builder \
            .master('local[*]') \
            .config("spark.jars",jarf)\
            .appName("Recon OrderId Filter") \
            .getOrCreate()
            #.enableHiveSupport() \
          
        
        


        filter_order_actv_table(spark, order_ids, reqId)

        spark.stop()
       # print(f"⚠️ Error during Spark filtering: {e}")


    # Define transformation logic based on data type
    def update_value(val):
        if isinstance(val, bool):
            return not val
        elif isinstance(val, int):
            return val + 100
        elif isinstance(val, float):
            return round(val + 0.100, 3)
        elif isinstance(val, str):
            try:
                # Skip date strings
                pd.to_datetime(val)
                return val
            except:
                return val + 'test'
        return val

    # Apply updates based on the mappings
    for item in data.get('results', []):
        for path in mappings:
            parts = path.split('.')
            if len(parts) != 2:
                continue  # ignore malformed paths

            parent, key = parts
            if parent in item and isinstance(item[parent], dict):
                if key in item[parent]:
                    original_value = item[parent][key]
                    updated_value = update_value(original_value)
                    item[parent][key] = updated_value
                    # Uncomment to debug:
                    # print(f"Updated {path}: {original_value} -> {updated_value}")

    # Save updated JSON
    with open(output_path, 'w') as f:
        json.dump(data, f, indent=4)

    return os.path.abspath(output_path)
    





def get_natural_key_mappings(excel_path):
    df = pd.read_excel(excel_path)
    df['NaturalKey'] = df['NaturalKey'].astype(str).str.strip().str.upper()
    df = df[(df['NaturalKey'] == 'Y')]
    return df['Mapping'].dropna().astype(str).str.strip().tolist()

def get_nested_value(obj, path):
    keys = path.split('.')
    for key in keys:
        if isinstance(obj, dict):
            obj = obj.get(key)
        else:
            return None
    return obj

def extract_order_ids_from_json_dynamic(json_path, mappings):
    with open(json_path, 'r') as f:
        data = json.load(f)
    order_ids = set()
    for item in data.get('results', []):
        print('mappings',mappings)
        for path in mappings:
            print('path', path)
            val = get_nested_value(item, path)
            if val is not None:
                order_ids.add(str(val))
                print('OrdeIdRetrived ',str(val))
    return list(order_ids)


def filter_order_actv_table(spark, order_ids, req_id):
    if not order_ids:
        print("No OrderIds found, skipping Spark filtering.")
        return
    df = spark.read.jdbc(
        url="jdbc:postgresql://localhost:5432/telusko",
        table="ORDER_ACTV",
        properties={"user": "postgres", "password": "1234", "driver": "org.postgresql.Driver"}
    )
    filtered = df.filter(col("OrderId").isin(order_ids))
    filtered.show();
    target_table = f"ORDER_ACTV_{req_id}"
    filtered.write.jdbc(
            url="jdbc:postgresql://localhost:5432/telusko",
            table=target_table,
            properties={"user": "postgres", "password": "1234", "driver": "org.postgresql.Driver"}
    )


    print(f"✅ Filtered Order_Actv written to: {target_table}")

# Execute hook logic

    