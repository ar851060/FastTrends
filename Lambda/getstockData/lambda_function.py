import json
import boto3
import requests
from decimal import *

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("stock_trends")

def lambda_handler(event, context):
    t = requests.get('https://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_2330.tw')
    r = json.loads(t.text)["msgArray"][0]["pz"]
    data = table.get_item(Key={"ID": 0})["Item"]
    data["sprice"] = Decimal(str(r))
    table.put_item(Item=data)
    
    return {"statusCode": 200, "body": r}