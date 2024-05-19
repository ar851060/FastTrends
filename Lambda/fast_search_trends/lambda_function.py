import json
from serpapi import GoogleSearch
import boto3
import os
from time import strftime
from datetime import datetime, timedelta, timezone
from decimal import *

client = boto3.client('bedrock-runtime')

modelId = 'anthropic.claude-3-sonnet-20240229-v1:0'
accept = 'application/json'
contentType = 'application/json'

def lambda_handler(event, context):
    
    dt = datetime.utcnow() + timedelta(hours=8)
    dt = dt.strftime("%H:%M")
    
    if not event['data']:
        return {
            'statusCode': 200,
            'body': {'score':"No Data", 'summary':"No Data", 'query_time':dt}
            }
        
    params = {
      "engine": "google_news",
      "q": event['data'],
      "api_key": os.environ['google_search_api_key'],
      'gl':'tw'
    }
    
    try:
        search = GoogleSearch(params)
        results = search.get_dict()
        news_results = results["news_results"]
    except:
        return {
            'statusCode': 200,
            'body': {'score':"No Data", 'summary':"No Data", 'query_time':dt}
            }
    
    title_collection = []

    for i in news_results:
      try:
        title_collection.append(i['title'])
      except:
        for j in i['stories']:
          title_collection.append(j['title'])
    
    prompt = f"""
      請將以下近期市場消息總結成一個三百字的文章 並且相關分析內容要與會影響到股價方面相關 文章摘要總結需與分數高低相關但不要提到標題
      標題:###
      {';'.join(title_collection)}
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
    
    
    return {
        'statusCode': 200,
        'body': {'summary':summary_text, 'query_time':dt}
    }
