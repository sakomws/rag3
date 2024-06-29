

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

{"real_time_sub_prompts":["- What is the current price of Tesla stocks?","- How have Tesla stocks been performing today?","","Non-realtime: ","- What is the historical performance of Tesla stocks?","- What factors influence the price of Tesla stocks?"],"non_real_time_sub_prompts":[]}% 

```

