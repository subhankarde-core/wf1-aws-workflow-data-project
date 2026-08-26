# Databricks notebook source
# MAGIC %md
# MAGIC ##Reading the files ariving in the raw_data folder

# COMMAND ----------

from pyspark.sql.functions import *

# COMMAND ----------


measurement_station_schema = "station_code INT, station_name STRING, address STRING, latitude DOUBLE, longitude DOUBLE"

measurement_station_df = spark.read.csv(
    's3://data-platform-240534892394-subhankar/wf1-aws-data-proj/raw_inputs/measurement_station/*.csv',
    header=True,
    schema=measurement_station_schema
)


measurement_item_schema='item_code INT, item_name STRING,unit_of_measurement STRING,good double,normal double,bad double,very_bad double'

measurement_item_df = spark.read.csv(
    's3://data-platform-240534892394-subhankar/wf1-aws-data-proj/raw_inputs/measurement_item/*.csv',
    header=True,
    schema=measurement_item_schema
)
measurement_schema='measurement_date TIMESTAMP, station_code INT,item_code INT, average_value DOUBLE, instrument_status INT'

measurement_df = spark.read.csv(
    's3://data-platform-240534892394-subhankar/wf1-aws-data-proj/raw_inputs/measurement_info/*.csv',
    header=True,
    schema=measurement_schema
)

# COMMAND ----------

measurement_station_df.display()

# COMMAND ----------

measurement_item_df.display()

# COMMAND ----------

measurement_df.display()

# COMMAND ----------

# MAGIC %md
# MAGIC ##Transformations if required

# COMMAND ----------

measurement_station_df=measurement_station_df.withColumn('latitude', col('latitude').try_cast('decimal(20, 16)')).withColumn('longitude', col('longitude').try_cast('decimal(20, 16)'))

# COMMAND ----------

measurement_df=measurement_df.withColumn('measurement_date', to_timestamp(col('measurement_date'), 'yyyy-MM-dd HH:mm:ss'))

# COMMAND ----------

# MAGIC %md
# MAGIC ##Writing the curated data to S3 in parquet format

# COMMAND ----------

measurement_station_df.write.format('parquet').mode('overwrite').save('s3://data-platform-240534892394-subhankar/wf1-aws-data-proj/curated_inputs/measurement_station/')

measurement_item_df.write.format('parquet').mode('overwrite').save('s3://data-platform-240534892394-subhankar/wf1-aws-data-proj/curated_inputs/measurement_item/')

measurement_df.write.format('parquet').mode('overwrite').save('s3://data-platform-240534892394-subhankar/wf1-aws-data-proj/curated_inputs/measurement_info/')
