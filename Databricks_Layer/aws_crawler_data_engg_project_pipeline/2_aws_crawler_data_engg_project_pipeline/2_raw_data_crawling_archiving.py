# Databricks notebook source
from datetime import datetime

date_part=datetime.now().strftime("%Y%m%d")

landing_path='s3://data-platform-240534892394-subhankar/wf1-aws-data-proj/raw_inputs'
archived_path=f's3://data-platform-240534892394-subhankar/wf1-aws-data-proj/raw_inputs/archive'

measurement_landing=f'{landing_path}/measurement_info'
measurement_archive=f'{archived_path}/measurement_info'

measurement_item_landing=f'{landing_path}/measurement_item'
measurement_item_archive=f'{archived_path}/measurement_item'

measurement_station_landing=f'{landing_path}/measurement_station'
measurement_station_archive=f'{archived_path}/measurement_station'


# COMMAND ----------

# MAGIC %md
# MAGIC ##Achiving Measurement files

# COMMAND ----------

file=dbutils.fs.ls(measurement_landing)

# Delete metadata files
#for file_info in file:
#    if "%SUCCESS" in file_info.name or "_committed%" in file_info.name or "_started%" in file_info.name:
#        print(f"Deleting: {file_info.path}")
#        dbutils.fs.rm(file_info.path, recurse=True)

# Move remaining files to archive
for file_info in file:
    dbutils.fs.mv(file_info.path,f'{measurement_archive}/date={date_part}/{file_info.name}',True)

# COMMAND ----------

# MAGIC %md
# MAGIC ##Achiving Measurement_item files

# COMMAND ----------

file=dbutils.fs.ls(measurement_item_landing)

# Delete metadata files
#for file_info in file:
#    if "%SUCCESS" in file_info.name or "_committed%" in file_info.name or "_started%" in file_info.name:
#        print(f"Deleting: {file_info.path}")
#        dbutils.fs.rm(file_info.path, recurse=True)

# Move remaining files to archive
for file_info in file:
    dbutils.fs.mv(file_info.path,f'{measurement_item_archive}/date={date_part}/{file_info.name}',True)

# COMMAND ----------

# MAGIC %md
# MAGIC ##Achiving Measurement_station files

# COMMAND ----------

file=dbutils.fs.ls(measurement_station_landing)

# Delete metadata files
#for file_info in file:
#    if "%SUCCESS" in file_info.name or "_committed%" in file_info.name or "_started%" in file_info.name:
#        print(f"Deleting: {file_info.path}")
#        dbutils.fs.rm(file_info.path, recurse=True)

# Move remaining files to archive
for file_info in file:
    dbutils.fs.mv(file_info.path,f'{measurement_station_archive}/date={date_part}/{file_info.name}',True)