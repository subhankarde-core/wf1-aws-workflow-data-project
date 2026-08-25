Table DDLs in Athena:

CREATE EXTERNAL TABLE IF NOT exists `souel_station`.`measurement`(
  measurement_date timestamp,
  station_code bigint,
  item_code bigint,
  average_value double,
  instrument_status bigint
)
STORED AS PARQUET
LOCATION 's3://data-platform-240534892394-subhankar/wf1-aws-data-proj/curated_inputs/measurement_info/';



CREATE EXTERNAL TABLE IF NOT exists `souel_station`.`measurement_item`(
  item_code int,
  item_name string,
  unit_of_measurement string,
  good double,
  normal double,
  bad double,
  very_bad double
)
STORED AS PARQUET
LOCATION 's3://data-platform-240534892394-subhankar/wf1-aws-data-proj/curated_inputs/measurement_item/';


CREATE EXTERNAL TABLE IF NOT exists `souel_station`.`measurement_station`(
station_code bigint,
station_name varchar(100),
address varchar(200),
latitude decimal(20,16),
longitude decimal(20,16)
)
STORED AS PARQUET
LOCATION 's3://data-platform-240534892394-subhankar/wf1-aws-data-proj/curated_inputs/measurement_station/'

CREATE EXTERNAL TABLE IF NOT exists `souel_station`.`measurement_summary`(
	measurement_date timestamp,
	station_name varchar(100),
	address varchar(200),
	latitude decimal(20,16),
	longitude decimal(20,16),
	SO2 double,
	NO2 double,
	O3 double,
	CO double,
	PM10 double,
	PM2.5 double
	)
STORED AS PARQUET
LOCATION 's3://data-platform-240534892394-subhankar/wf1-aws-data-proj/curated_inputs/measurement_station/'
