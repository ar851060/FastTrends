import json
import boto3

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("stock_trends")

def lambda_handler(event, context):
    response = table.get_item(Key={"ID": 0})["Item"]
    
    return {"statusCode": 200, "body": response}