import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when


def fetch_json_from_api(url, payload):
    headers = {
        'Content-Type': 'application/json',  
    }
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        print(response.json());
        return response.json()  
    else:
        raise Exception(f"Error fetching data from API. Status code: {response.status_code}")
payload = {
        "key": "value"  
    }

print('hello1')

url_json1 = "http://localhost:8000/get_cloud_data/"
url_json2 = "http://localhost:8000/get_kafka_data/"
url_json3 = "http://localhost:8000/get_impala_data/"
url_json4 = "http://localhost:8000/get_gemfire_data/"


json1_data = fetch_json_from_api(url_json1, payload)
json2_data = fetch_json_from_api(url_json2, payload)
json3_data = fetch_json_from_api(url_json3, payload)
json4_data = fetch_json_from_api(url_json4, payload)
print(json1_data);


spark = SparkSession.builder.appName('JsonComparison').master('local[*]').enableHiveSupport().getOrCreate()

spark.sparkContext.setLogLevel("ERROR")


json1_df = spark.read.json(spark.sparkContext.parallelize([json1_data]))
json2_df = spark.read.json(spark.sparkContext.parallelize([json2_data]))
json3_df = spark.read.json(spark.sparkContext.parallelize([json3_data]))
json4_df = spark.read.json(spark.sparkContext.parallelize([json4_data]))

print('hello2')

columns = json1_df.columns
print('hello3')

df = json1_df.join(json2_df, "name", "outer") \
             .join(json3_df, "name", "outer") \
             .join(json4_df, "name", "outer")


comparison_columns = []
for column in columns:
   
    comparison_columns.append(
        {
            "column": column,
            "json1_value": col(f"json1.{column}"),
            "json2_value": col(f"json2.{column}"),
            "json3_value": col(f"json3.{column}"),
            "json4_value": col(f"json4.{column}"),
            "status": when(
                (col(f"json1.{column}") != col(f"json2.{column}")) |
                (col(f"json1.{column}") != col(f"json3.{column}")) |
                (col(f"json1.{column}") != col(f"json4.{column}")),
                "Mismatch"
            ).otherwise("Match"),
            "code": when(
                (col(f"json1.{column}") != col(f"json2.{column}")),
                "1011"
            ).when(
                (col(f"json1.{column}") != col(f"json3.{column}")),
                "1101"
            ).when(
                (col(f"json1.{column}") != col(f"json4.{column}")),
                "1110"
            ).otherwise("1111")
        }
    )
print('hello4.0')
# Create the final DataFrame with all comparisons and status
final_columns = []
for comp in comparison_columns:
    final_columns.append(comp["column"])
    final_columns.append(comp["json1_value"])
    final_columns.append(comp["json2_value"])
    final_columns.append(comp["json3_value"])
    final_columns.append(comp["json4_value"])
    final_columns.append(comp["status"])
    final_columns.append(comp["code"])

# Select the final comparison DataFrame
comparison_df = df.select(*final_columns)
print('hello41')
# Show the result with comparison indicators
comparison_df.show()
print('hello42')
# Optionally, save the result back to a file
comparison_df.write.json("comparison_output.json")

print('hello43')
