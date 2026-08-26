import boto3

s3 = boto3.client("s3")


def lambda_handler(event, context):

    bucket = "data-platform-240534892394-subhankar"

    base_path = "wf1-aws-data-proj/curated_inputs/"

    folders = [
        "measurement_info/",
        "measurement_item/",
        "measurement_station/"
    ]

    for folder in folders:

        prefix = base_path + folder

        response = s3.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix
        )

        if "Contents" in response:

            for obj in response["Contents"]:

                s3.delete_object(
                    Bucket=bucket,
                    Key=obj["Key"]
                )

                print(f"Deleted: {obj['Key']}")

    return {
        "statusCode": 200,
        "message": "Files deleted. Folder prefixes retained."
    }