from pyspark.sql import SparkSession


spark = SparkSession.builder.appName("example").master('local[*]').getOrCreate()
data = [("Alice", 34), ("Bob", 45), ("Catherine", 29)]
columns = ["Name", "Age"]
df = spark.createDataFrame(data, schema=columns)
df.show()