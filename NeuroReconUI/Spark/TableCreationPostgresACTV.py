from pyspark.sql import SparkSession
import os
import psycopg2
from pyspark.sql import Row
from datetime import datetime

# Setup for jars
jar_dir = os.path.join(os.getcwd(), 'Jars')  # Adjust the path as needed
hive_jar_files = os.path.join(jar_dir, 'postgresql-42.7.5.jar')

# Initialize Spark session
spark = SparkSession.builder \
    .master('local[*]') \
    .appName("PostgresExample") \
    .config("spark.jars", hive_jar_files) \
    .getOrCreate()

# Database connection properties
db_url = "jdbc:postgresql://localhost:5432/telusko"
db_user = "postgres"
db_password = "1234"

# Create PostgreSQL connection using psycopg2
conn = psycopg2.connect(
    dbname="telusko",
    user=db_user,
    password=db_password,
    host="localhost",
    port="5432"
)


# Create a cursor from the connection
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS ORDER_ACTV")
# Create table query
create_table_query = """
CREATE TABLE IF NOT EXISTS ORDER_ACTV (
    OrderId INTEGER PRIMARY KEY,
    OrderName VARCHAR(255),
    OrderPrice BIGINT,
    OrderDate TIMESTAMP,
    OrderType VARCHAR(100),
    AddressLine1 VARCHAR(255),
    PinCode INTEGER,
    State VARCHAR(100),
    District VARCHAR(100),
    PhoneNumber BIGINT
);
"""

# Execute the table creation query
cursor.execute(create_table_query)

# Commit the changes and close the connection
conn.commit()
cursor.close()
conn.close()


from pyspark.sql.types import StructType, StructField, IntegerType, StringType, LongType, TimestampType
from pyspark.sql import Row
from datetime import datetime

# Define schema
schema = StructType([
    StructField("OrderId", IntegerType(), True),
    StructField("OrderName", StringType(), True),
    StructField("OrderPrice", LongType(), True),
    StructField("OrderDate", TimestampType(), True),
    StructField("OrderType", StringType(), True),
    StructField("AddressLine1", StringType(), True),
    StructField("PinCode", IntegerType(), True),
    StructField("State", StringType(), True),
    StructField("District", StringType(), True),
    StructField("PhoneNumber", LongType(), True)
])

# Sample data
data = [
    (111, "Order1", 1000, datetime.strptime("2023-09-01 10:10:10", "%Y-%m-%d %H:%M:%S"), 
     "Online", "Street A", 123456, "State1", "District1", 1234567890),
    (222, "Order2", 2000, datetime.strptime("2023-09-02 11:12:12", "%Y-%m-%d %H:%M:%S"), 
     "Offline", "Street B", 654321, "State2", "District2", 9876543210),
    (3333, "Order3", 1500, datetime.strptime("2023-09-03 09:09:09", "%Y-%m-%d %H:%M:%S"), 
     "Online", "Street C", 456789, "State1", "District3", 1928374650),
    (444, "Order4", 2500, datetime.strptime("2023-09-04 12:12:12", "%Y-%m-%d %H:%M:%S"), 
     "Offline", "Street D", 789456, "State3", "District1", 1231231230),
    (555, "Order5", 3000, datetime.strptime("2023-09-05 13:30:30", "%Y-%m-%d %H:%M:%S"), 
     "Online", "Street E", 321654, "State2", "District2", 4564564560)
]

# Create DataFrame
df = spark.createDataFrame(data, schema=schema)

# Write to PostgreSQL
df.write.jdbc(
    url="jdbc:postgresql://localhost:5432/telusko",
    table="orders",
    mode="append",
    properties={"user": "postgres", "password": "1234", "driver": "org.postgresql.Driver"}
)