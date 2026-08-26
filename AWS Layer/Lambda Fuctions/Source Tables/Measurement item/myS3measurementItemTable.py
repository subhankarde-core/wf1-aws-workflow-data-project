import boto3

def lambda_handler(event, context):
    # Initialize the Athena client
    athena_client = boto3.client('athena')
    
    # Define your DDL query to create the table
    create_table_query = """
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
    """
    
    # Execute the query
    response = athena_client.start_query_execution(
        QueryString=create_table_query,
        QueryExecutionContext={
            'Database': 'souel_station'  # Your Glue/Athena database name
        },
        ResultConfiguration={
            'OutputLocation': 's3://data-platform-240534892394-subhankar/wf1-aws-data-proj/curated_results/'  # S3 bucket for logs
        }
    )
    
    # Returns the Query Execution ID to track status if needed
    return {
        'statusCode': 200,
        'body': f"Table creation initiated. Execution ID: {response['QueryExecutionId']}"
    }
