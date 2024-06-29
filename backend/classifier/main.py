import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai
from dotenv import load_dotenv

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
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You will be given a question from a financial analyst about some financial documents. Please create sub-questions that can help get the information needed to answer the user question. The sub questions may correspond to real time or non-real time data sources. Return always json output whose keys are 'non_real_time' and 'real_time' and values are a list of sub question strings. Example: {\"real_time\": [\"subprompt1\", \"subprompt2\"], \"non_real_time\": [\"subprompt3\", \"subprompt4\"]}"},
                {"role": "user", "content": prompt.prompt}
            ]
        )

        classification = response.choices[0].message['content'].strip()
        # Assuming the response is already in the desired JSON format
        return classification
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)