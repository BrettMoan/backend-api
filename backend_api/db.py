import boto3
import os

dynamodb = boto3.resource(
    "dynamodb",
    region_name=os.getenv("AWS_REGION", "us-east-1")
)
tasks_table = dynamodb.Table(os.getenv("TASKS_TABLE_NAME", "tasks"))
