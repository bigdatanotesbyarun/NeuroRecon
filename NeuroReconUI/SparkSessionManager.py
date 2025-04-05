from pyspark.sql import SparkSession

# Initialize a Spark session
spark = SparkSession.builder.appName("example").getOrCreate()

# Sample data
data = [("Alice", 34), ("Bob", 45), ("Catherine", 29)]

# Column names
columns = ["Name", "Age"]

# Create DataFrame
df = spark.createDataFrame(data, schema=columns)

# Show DataFrame
df.show()




# Filter data
df_filtered = df.filter(df.Age > 30)
df_filtered.show()

# Select specific columns
df_selected = df.select("Name")
df_selected.show()
