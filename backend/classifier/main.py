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
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You will be given a question from a financial analyst about some financial documents. Please create sub-questions that can help get the information needed to answer the user question. The sub questions may correspond to real time or non-real time data sources. Return a json whose keys are 'non_real_time' and 'real_time' and values are a list of sub question strings. Example: {\"realtime\": [\"subprompt1\", \"subprompt2\"], \"non_realtime\": [\"subprompt3\", \"subprompt4\"]}"},
                {"role": "user", "content": prompt.prompt}
            ]
        )

        classification = response.choices[0].message['content'].strip()
        return classification

        real_time_sub_prompts = []
        non_real_time_sub_prompts = []
        
        # Simple parsing logic to split real-time and non-realtime sub-prompts
        if "Non-realtime sub-prompts:" in classification:
            real_time_part, non_real_time_part = classification.split("Non-realtime sub-prompts:")
            real_time_sub_prompts = real_time_part.strip().split('\n')[1:]
            non_real_time_sub_prompts = non_real_time_part.strip().split('\n')[1:]
        else:
            real_time_sub_prompts = classification.strip().split('\n')[1:]

        return {
            "real_time_sub_prompts": real_time_sub_prompts,
            "non_real_time_sub_prompts": non_real_time_sub_prompts
        }
    except openai.error.OpenAIError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)