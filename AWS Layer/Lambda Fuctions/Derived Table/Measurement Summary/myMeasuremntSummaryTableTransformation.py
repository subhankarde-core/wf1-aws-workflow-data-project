import boto3
import time

athena_client = boto3.client('athena')

def lambda_handler(event, context):
    
    database = "souel_station"
    target_table = "measurement_summary"
    s3_output_location = "s3://data-platform-240534892394-subhankar/wf1-aws-data-proj/curated_results/"
    
    # 2. Construct the CTAS SQL Query
    # This simultaneously creates the table schema and populates it with data
    query_string = """
    CREATE TABLE souel_station.measurement_summary
    WITH (
        format = 'PARQUET',
        external_location = 's3://data-platform-240534892394-subhankar/wf1-aws-data-proj/curated_inputs/measurement_summary'
    ) AS 
    SELECT m.measurement_date, ms.station_code, ms.station_name, ms.address, ms.latitude, ms.longitude, 
     MAX(CASE WHEN mi.item_code=1 THEN m.average_value END) as SO2,
     MAX(CASE WHEN mi.item_code=3 THEN m.average_value END) as NO2,
     MAX(CASE WHEN mi.item_code=5 THEN m.average_value END) as CO,
     MAX(CASE WHEN mi.item_code=6 THEN m.average_value END) as O3,
     MAX(CASE WHEN mi.item_code=8 THEN m.average_value END) as PM10,
     MAX(CASE WHEN mi.item_code=9 THEN m.average_value END) as "PM2.5"
     FROM
     "souel_station"."measurement" m 
     JOIN "souel_station"."measurement_item" mi 
     on m.item_code=mi.item_code
     JOIN "souel_station"."measurement_station" ms
     ON m.station_code=ms.station_code
     GROUP BY m.measurement_date, ms.station_code, ms.station_name, 
     ms.address, ms.latitude, ms.longitude
    """
    
    try:
        # 3. Start the Athena Query Execution
        response = athena_client.start_query_execution(
            QueryString=query_string,
            QueryExecutionContext={'Database': database},
            ResultConfiguration={'OutputLocation': s3_output_location}
        )
        query_execution_id = response['QueryExecutionId']
        print(f"Query started with Execution ID: {query_execution_id}")
        
        # 4. Poll for results (Athena queries are asynchronous)
        while True:
            status_response = athena_client.get_query_execution(
                QueryExecutionId=query_execution_id
            )
            status = status_response['QueryExecution']['Status']['State']
            
            if status in ['SUCCEEDED']:
                print(f"Table {target_table} created and populated successfully!")
                return {
                    'statusCode': 200,
                    'body': f"Success. Table {target_table} created."
                }
            elif status in ['FAILED', 'CANCELLED']:
                reason = status_response['QueryExecution']['Status'].get('StateChangeReason', 'Unknown error')
                raise Exception(f"Athena query {status}. Reason: {reason}")
            
            # Wait for 2 seconds before polling again to prevent throttling
            time.sleep(2)
            
    except Exception as e:
        print(f"Error executing query: {str(e)}")
        raise e