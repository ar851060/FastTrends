# Fast Trends

這個專案是製作於由digitimes以及AWS在2024/05/18-19合辦的【[雲湧智生-台灣生成式AI應用黑客松競賽](https://www.digitimes.com.tw/seminar/Hackathon_20240518/)】中的成品。    

This project was made in the AI Wave: Taiwan Generative AI Applications Hackathon held by Digitimes and AWS, the information on this competition is on this [website](https://www.digitimes.com.tw/seminar/Hackathon_20240518/).

## Core value

利用生成式AI技術，經由自動分析及評估與股票相關的新聞，提供精確的影響評分和摘要，幫助投資者做出更明智的決策。生成式AI模型將自動抓取和分析股票相關的新聞和社交媒體內容，並進行情感分析和情境分析，對新聞內容進行評分，評估其對股價的正面或負面影響。基於分析結果，生成簡潔的新聞摘要和綜合評分，供投資者快速閱讀和理解。
自動化的新聞分析技術將大幅減少人工分析的時間和人力成本，使分析師能夠專注於更高價值的任務。此外，生成式AI技術將推動開發簡短且高效的分析報告，也能幫助非專業投資人快速理解市場趨勢和機會。通過這些簡短的分析報告，投資者能夠迅速進行有效的決策，及時應對市場變化，從而降低決策錯誤帶來的財務風險。

Utilizing generative AI technology, it automatically analyzes and evaluates stock-related news to provide precise impact scores and summaries to help investors make more informed decisions. The generative AI model will automatically capture and analyze stock-related news and social media content, conduct sentiment analysis and situational analysis, score the news content, and evaluate its positive or negative impact on stock prices. Based on the analysis results, concise news summaries and comprehensive scores are generated for investors to quickly read and understand.
Automated news analysis technology will significantly reduce the time and labor costs of manual analysis, allowing analysts to focus on higher-value tasks. In addition, generative AI technology will promote the development of short and efficient analysis reports, and can also help non-professional investors quickly understand market trends and opportunities. Through these short analysis reports, investors can quickly make effective decisions and respond to market changes on time, thus reducing the financial risks caused by decision-making errors.

## Scoring Calculation Rule

我們會收集近期在Google News裡面最相關也最受關注的前100筆新聞，並且利用一些加權平均的方式來結合出趨勢分數的部分。分數規則的主要是利用AI來判讀該新聞對於股市的影響為正向、負向、以及中立，給於+1、-1、以及0的分數。再利用Google News裡面的新聞排序來加權，基本上排的越前面、分數越高。

We will collect the top 100 most relevant and popular news in Google News recently, and use some weighted average methods to combine the trend scores. The scoring rule mainly uses AI to judge the impact of the news on the stock market as positive, negative, or neutral and gives scores of +1, -1, and 0. Then use the news ranking in Google News to weight it. The higher the ranking, the higher the score.

![Scoring Rule](https://github.com/ar851060/FastTrends/blob/main/report/P04.png)

## How to use it

分成兩個部分：    
There are two parts to this project:

1. Stock Trends Dashboards

   ![Stock Trends Dashboards](https://github.com/ar851060/FastTrends/blob/main/report/P03.png)
   
   這部分主要是關注重要的投資標的，定期更新資料，呈現出目前的趨勢、一小時的變化、以及目前股價價格並且呈現2個小時內的趨勢。同時也顯示出近期新聞的重點摘要。
   
   This part mainly focuses on important investment targets, regularly updates the information, shows the current trend, one-hour changes, and the current stock price, and shows the trend within 2 hours. It also displays a summary of recent news.
   
3. Fast Trends

   ![Fast Trends](https://github.com/ar851060/FastTrends/blob/main/report/P05.png)

   搜尋某投資標的，可以快速得到該標的的近期新聞的重點摘要。

   Search for an investment target and you can quickly get a summary of recent news about the target.

## AWS Structure

我們在這個專案使用了以下AWS服務： Amplify, API Gateway, Lambda, IAM, EventBridge, Bedrock, DynamoDB

The services we used in this project are: Amplify, API Gateway, Lambda, IAM, EventBridge, Bedrock, DynamoDB

* Amplify 作為我們的網頁前端。 Amplify serves as the frontend of our service
* API Gateway 作為Lambda以及Amplify的連結。 API Gateway serves as the connection between Lambda and Amplify.
* Lambda 作為核心演算法的處理器。 Lambda serves as the core algorithm running place.
* IAM 作為各項AWS服務的權限控制。 IAM serves as the permission control for all kinds of services in AWS.
* EventBridge 作為定時觸發lambda爬蟲的機制。 EventBridge serves as the regular timer trigger for Lambda.
* Bedrock 作為AI模型服務平台，這次的專案我們使用Claude 3 Sonnet。 Bedrock serves as a platform providing AI service, we use Claude 3 Sonnet in this project.
* DynamoDB 作為資料庫存取計算過後以及爬蟲下來的資訊儲存處。 DynamoDB serves as a database to access the information stored after calculation and crawling.

![AWS Structure](https://github.com/ar851060/FastTrends/blob/main/report/P06.png)

## Report

我們把現場報告的簡報放在[https://github.com/ar851060/FastTrends/blob/main/report/Fast%20Trends.pdf](https://github.com/ar851060/FastTrends/blob/main/report/Fast%20Trends.pdf)

The report we present in competition is [here](https://github.com/ar851060/FastTrends/blob/main/report/Fast%20Trends.pdf)
