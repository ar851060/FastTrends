import json
from serpapi import GoogleSearch
import boto3
import os
from time import strftime
from datetime import datetime, timedelta, timezone
from decimal import *

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('stock_trends')
client = boto3.client('bedrock-runtime')

modelId = 'anthropic.claude-3-sonnet-20240229-v1:0'
accept = 'application/json'
contentType = 'application/json'

def lambda_handler(event, context):
    
    dt = datetime.utcnow() + timedelta(hours=8)
    dt = dt.strftime("%H:%M")
    params = {
      "engine": "google_news",
      "q": "台積電",
      "api_key": os.environ['google_search_api_key']
    }
    
    search = GoogleSearch(params)
    results = search.get_dict()
    news_results = results["news_results"]
    news_score = 0
    
    
    for news in news_results:
        weight = (5-int(news['position'])//21)+(int(news['position'])%21-1)*0.01
        
        prompt = f"""
        According to the following news title, please give reponse that what kind of impact for the company's stock.
        You only need to reply me the three possible answer: ['positive','negative','neutral'].
        ###
        {news['title']}
        """
        claude_input = json.dumps({
                            "anthropic_version": "bedrock-2023-05-31",    
                            "max_tokens": 20,
                            "system": "According to the following news title, please give reponse that what kind of impact for the company's stock. You only need to reply me the three possible answer: ['postitve','negative','neutral'].",    
                            "messages": [
                                {
                                    "role": "user",
                                    "content": [
                                        { "type": "text", "text": prompt }
                              ]
                                }
                            ],
                            "temperature": 0.5,
                            "top_p": 1,
                            "top_k": 10,
                            "stop_sequences": []
                        })
        response = client.invoke_model(body=claude_input, modelId=modelId, accept=accept, contentType=contentType)
        response_body = json.loads(response.get("body").read())
        response_text = response_body['content'][0]['text']
        
        if 'positive' in response_text:
            res = 1
        elif 'negative' in response_text:
            res = -1
        else:
            res = 0
        
        news_score += weight * res 
    
    final_score = (news_score + 290.5)/581*100
    
    prompt = f"""
    分數是{final_score}(0~100, 0 是最差，100是最好），請將以下近期市場消息總結成一個三百字的文章 並且相關分析內容要與會影響到股價方面相關 文章摘要總結需與分數高低相關但不要提到根據分數以及標題
    標題:###
    {';'.join([i['title'] for i in news_results])}
    ###
    """
    claude_input = json.dumps({
                            "anthropic_version": "bedrock-2023-05-31",    
                            "max_tokens": 2000,
                             "messages": [
                                {
                                    "role": "user",
                                    "content": [
                                        { "type": "text", "text": prompt }
                              ]
                                }
                            ],
                            "temperature": 0.9,
                            "top_p": 1,
                            "top_k": 250,
                            "stop_sequences": []
                        })
    response = client.invoke_model(body=claude_input, modelId=modelId, accept=accept, contentType=contentType)
    response_body = json.loads(response.get("body").read())
    summary_text = response_body['content'][0]['text']
    
    history_record = table.get_item(Key = {'ID':0})['Item']
    
    history_record['percentage'] = (Decimal(str(final_score))-history_record['cpoint'][-4])/history_record['cpoint'][-4]
    history_record['point'] = Decimal(str(final_score))
    history_record['summary'] = summary_text
    
    
    cpoint_list = history_record['cpoint']
    if len(cpoint_list) > 7:
        del cpoint_list[0]
    cpoint_list.append(Decimal(str(final_score)))
    history_record['cpoint'] = cpoint_list
    
    ctime_list = history_record['ctime']
    if len(ctime_list) > 7:
        del ctime_list[0]
    ctime_list.append(dt)
    history_record['ctime'] = ctime_list
    
    table_response = table.put_item(Item=history_record)
    
    return {
        'statusCode': 200,
        'body': json.dumps({})
    }
