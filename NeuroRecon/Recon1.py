import pandas as pd
import json
import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lit, when
from datetime import datetime
from django.conf import settings
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType



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


# Load the Excel file and sheet
excel_file = 'Staging\\DataModel\\OrderDataModel.xlsx'  # Path to your uploaded Excel file
df = pd.read_excel(excel_file)

# Extract the column names, mappings, and data types from the 'Destinationtype' column
column_names = df['ColumnName'].tolist()  # Get all ColumnNames
mappings = df['Mapping'].tolist()  # Get all Mappings
data_types = df['Destinationtype'].tolist()  # Get all DataTypes from the 'Destinationtype' column

# Load the JSON file (Product.json)
json_file = 'Staging\\Incoming\\Product\\Product.json'  # Path to your uploaded JSON file
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
spark = SparkSession.builder.appName('JsonComparison').master('local[*]').config(
    "spark.jars", "NeuroReconUI\\Jar\\postgresql-42.7.5.jar").enableHiveSupport().getOrCreate()

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
            lit(request_id).alias("RequestID")
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
# DATABASE_NAME = settings.DATABASES['default']['NAME']  # 'NAME' is the database name
# DATABASE_USER = settings.DATABASES['default']['USER']  # 'USER' is the username
# DATABASE_PASSWORD = settings.DATABASES['default']['PASSWORD']  # 'PASSWORD' is the password
# DATABASE_HOST = settings.DATABASES['default']['HOST']  # 'HOST' is the host, e.g., 'localhost'

# Define JDBC URL for PostgreSQL
#jdbc_url = f"jdbc:postgresql://{DATABASE_HOST}:5432/{DATABASE_NAME}"
jdbc_url = "jdbc:postgresql://localhost:5432/telusko"
# Write the DataFrame to PostgreSQL
final_df.write \
    .format("jdbc") \
    .option("url", jdbc_url) \
    .option("dbtable", "neuroreconui_reconresult") \
    .option("user", "postgres") \
    .option("password", "1234") \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
    .save()
print('Data Written')
