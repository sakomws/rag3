

1. Install the deps:
```
pip3 install -r requirements.txt
```


2. Run the server:
```
uvicorn main:app --reload
```

2. Query:
```
curl -X POST "http://localhost:8000/classify" -H "Content-Type: application/json" -d '{"prompt": "Your prompt here"}'

"{\"real_time\": [\"What is Tesla's current stock price?\", \"What are the latest news or events affecting Tesla's stock price?\", \"What is the current trading volume of Tesla's stock?\", \"What are the latest analyst ratings for Tesla's stock?\"], \"non_real_time\": [\"What has been the historical performance of Tesla's stock over the past year?\", \"What is Tesla's price-to-earnings ratio?\", \"What is Tesla's market capitalization?\", \"What are the key financial metrics (revenue, profit, etc.) from Tesla's latest quarterly report?\", \"What is Tesla's stock performance compared to its industry or sector?\", \"What significant announcements has Tesla made recently (e.g., product launches, earnings calls)?\"]}"%

```

