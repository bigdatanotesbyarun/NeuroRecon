import requests
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when
from pyspark.sql.functions import lit, when, col, struct, explode
from pyspark.sql.functions import lit, when, col, struct, explode, array
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import lit, col, when
from datetime import datetime


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


spark = SparkSession.builder.appName('JsonComparison').master('local[*]').config("spark.jars", "NeuroReconUI\\Jar\\postgresql-42.7.5.jar").enableHiveSupport().getOrCreate()

spark.sparkContext.setLogLevel("ERROR")


df1 = spark.read.json(spark.sparkContext.parallelize([json1_data]))
df2 = spark.read.json(spark.sparkContext.parallelize([json2_data]))
df3 = spark.read.json(spark.sparkContext.parallelize([json3_data]))

# Step 3: Join on the key (SMCP)
joined = df1.alias("df1") \
    .join(df2.alias("df2"), on="SMCP", how="outer") \
    .join(df3.alias("df3"), on="SMCP", how="outer")

# Step 4: Generate a dummy Request ID
request_id = f"req{datetime.now().strftime('%Y%m%d%H%M%S')}"

# Step 5: Compare field by field and prepare recon output
fields = ["Status", "Isin"]
recon_data = []

for field in fields:
    recon_data.append(
        joined.select(
            col("SMCP").alias("JoinKey"),                 # JoinKey FIRST
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

final_df.write \
    .format("jdbc") \
    .option("url", "jdbc:postgresql://localhost:5432/telusko") \
    .option("dbtable", "neuroreconui_reconresult") \
    .option("user", "postgres") \
    .option("password", "1234") \
    .option("driver", "org.postgresql.Driver") \
    .mode("append") \
    .save()
print('Data Written')
