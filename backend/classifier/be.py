from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

app = FastAPI()

openai.api_key = 'your-openai-api-key'

class Prompt(BaseModel):
    prompt: str

@app.post("/classify")
async def classify_prompt(prompt: Prompt):
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Classify the following prompt into real-time and non-realtime sub-prompts:\n\n{prompt.prompt}\n\nReal-time sub-prompts:\n1.",
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.7
        )

        classification = response.choices[0].text.strip()
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
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)