import boto3
import urllib.parse
from datetime import datetime

date_part=datetime.now().strftime("%Y%m%d")

s3 = boto3.client('s3')
# Source location
SOURCE_BUCKET = "data-platform-240534892394-subhankar"
SOURCE_PREFIX = (
    "wf1-aws-data-proj/"
    "curated_inputs/"
    "measurement_item/"
)

# Destination location
DESTINATION_BUCKET = "data-platform-240534892394-subhankar"
DESTINATION_PREFIX = (
    "wf1-aws-data-proj/"
    "curated_inputs/"
    "archive/"
    "measurement_item/"
)

def lambda_handler(event, context):
    try:

        # Destination partition
        destination_prefix = (
            f"{DESTINATION_PREFIX}"
            f"date={date_part}/"
        )

        print(
            f"Scanning source: "
            f"s3://{SOURCE_BUCKET}/{SOURCE_PREFIX}"
        )

        print(
            f"Archive destination: "
            f"s3://{DESTINATION_BUCKET}/{destination_prefix}"
        )

        # List objects in source prefix
        response = s3.list_objects_v2(
            Bucket=SOURCE_BUCKET,
            Prefix=SOURCE_PREFIX
        )

        objects = response.get("Contents", [])

        if not objects:
            print("No files found in source location.")

            return {
                "statusCode": 200,
                "body": "No files found to archive."
            }

        moved_files = 0

        for obj in objects:

            source_key = obj["Key"]

            # Ignore folder itself
            if source_key.endswith("/"):
                continue

            # Extract filename
            file_name = source_key.split("/")[-1]

            destination_key = (
                f"{destination_prefix}"
                f"{file_name}"
            )

            print(
                f"Moving: "
                f"s3://{SOURCE_BUCKET}/{source_key}"
            )

            print(
                f"To: "
                f"s3://{DESTINATION_BUCKET}/{destination_key}"
            )

            # --------------------------------------------
            # Step 1: Copy
            # --------------------------------------------

            s3.copy_object(
                CopySource={
                    "Bucket": SOURCE_BUCKET,
                    "Key": source_key
                },
                Bucket=DESTINATION_BUCKET,
                Key=destination_key
            )

            print(f"Copied successfully: {file_name}")

            # --------------------------------------------
            # Step 2: Delete source
            # --------------------------------------------

            #s3.delete_object(
            #    Bucket=SOURCE_BUCKET,
            #    Key=source_key
            #)

            #print(f"Deleted source: {file_name}")

            moved_files += 1

        print(
            f"Successfully moved {moved_files} file(s)."
        )

        return {
            "statusCode": 200,
            "body": (
                f"Successfully moved "
                f"{moved_files} file(s) to "
                f"date={date_part}"
            )
        }

    except Exception as e:

        print(f"Error: {str(e)}")

        raise
