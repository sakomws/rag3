import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import yfinance as yf

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

# Set OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

class Prompt(BaseModel):
    prompt: str

@app.post("/classify")
async def classify_prompt(prompt: Prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You will be given a question from a financial analyst about some financial documents. Please create sub-questions that can help get the information needed to answer the user question. The sub questions may correspond to real time or non-real time data sources. Return human readable string output with 3 keys: 'non_real_time', 'real_time' and 'company_ticker'. The values are a list of sub question strings. Example: {\"real_time\": [\"subprompt1\", \"subprompt2\"], \"non_real_time\": [\"subprompt3\", \"subprompt4\"], \"company_ticker\": [\"AAPL\", \"GOOGL\"]}"},
                {"role": "user", "content": prompt.prompt}
            ]
        )

        classification = response.choices[0].message['content'].strip()
        return classification
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

@app.get("/stock/{ticker}")
async def get_stock_data(ticker: str):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period="1d").to_dict()
        # Extract relevant stock data
        stock_info = {
            "close": data["Close"],
            "open": data["Open"],
            "high": data["High"],
            "low": data["Low"],
            "volume": data["Volume"]
        }
        return stock_info
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching stock data: {str(e)}")

@app.post("/reply")
async def reply(prompt: Prompt):
    try:
        # Step 1: Get the classification of the prompt
        classification_response = await classify_prompt(prompt)
        classification_data = eval(classification_response)  # Convert string to dictionary

        # Step 2: Extract the company ticker and real-time questions
        real_time_questions = classification_data.get("real_time", [])
        non_real_time_questions = classification_data.get("non_real_time", [])
        company_tickers = classification_data.get("company_ticker", [])

        stock_data = {}
        for ticker in company_tickers:
            # Step 3: Get the stock data for each ticker
            stock_data[ticker] = await get_stock_data(ticker)

        # Step 4: Answer the real-time questions using the stock data
        real_time_answers = []
        for question in real_time_questions:
            answer_response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Answer the following financial question using the provided data. Show data sources in reply include PDT hour and min. Output should be human readable. Example: 'The stock price of AAPL is $100 at 2:30 PM PDT.'"},
                    {"role": "user", "content": f"Question: {question}"},
                    {"role": "assistant", "content": f"Data: {stock_data}"}
                ]
            )
            answer = answer_response.choices[0].message['content'].strip()
            real_time_answers.append({"prompt: ": question, "result: ": answer})

        return {
            # "classification": {
            #     "real_time": real_time_questions,
            #     "non_real_time": non_real_time_questions,
            #     "company_ticker": company_tickers
            # },
            # "stock_data": stock_data,
            "real_time_answers": real_time_answers
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)