from pyspark.sql import SparkSession
import os
import sys
import pyspark





hive_site_xml_path = os.path.join(os.getcwd(), 'NeuroReconUI', 'Spark', 'hive-site.xml')
hive_warehouse_path = os.path.join(os.getcwd(), "NeuroReconUI", "Spark", "WareHouse") 

jar_dir = os.path.join(os.getcwd(),  'Jars')  # Adjust the path as needed
hive_jar_files = os.path.join(jar_dir, 'hive-exec-3.1.2.jar') + ',' + os.path.join(jar_dir, 'hive-metastore-3.1.2.jar') +','+os.path.join(jar_dir, 'datanucleus-core-6.0.10.jar')
print(jar_dir)


spark = SparkSession.builder \
    .appName("NeuroReconUI_Hive_Spark") \
    .master('local[*]')\
    .config("spark.jars", hive_jar_files) \
    .config("spark.sql.warehouse.dir", "file:///" + hive_warehouse_path) \
    .config("spark.hadoop.hive.metastore.uris", "thrift://localhost:9083") \
    .config("spark.hadoop.hive-site.xml", hive_site_xml_path) \
    .enableHiveSupport() \
    .getOrCreate()

print("Python Version:", sys.version)
print("pyspark.__version__:",pyspark.__version__)  # PySpark version
print("spark.version",spark.version)    


print(hive_site_xml_path);
print(hive_warehouse_path);

# create_table_sql = """
# CREATE TABLE IF NOT EXISTS orders_table (
#     OrderId INT,
#     OrderPrice BIGINT,
#     OrderDate TIMESTAMP,
#     PinCode INT,
#     PhoneNumber INT
# ) STORED AS PARQUET
# """

# Execute SQL query
spark.sql("SELECT 1")

# Verify table creation
#spark.sql("SHOW TABLES").show()

print(spark)