import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import google.generativeai as genai


load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

# Configure Google Generative AI with AgiPI key
genai.configure(api_key=api_key)

app = FastAPI()

class CommitMessage(BaseModel):
    query: str

@app.post("/generate-text")
async def generate_text(commit: CommitMessage):
    try:
        roast_prompt = f"""You are a snarky code review AI that ruthlessly roasts commit messages.

Analyze this commit message and generate a hilarious, savage roast:

Commit Message: "{commit.message}"

Roast Criteria:
- Assess the commit message's clarity
- Identify any vagueness or laziness
- Point out potential code sins
- Be witty and brutally honest

Format your response as:
🔥 Roast Level: [Spice Level 1-5]
💥 Roast: [Savage critique of the commit message]
🚨 Code Advice: [Constructive suggestion]

Remember: Maximum snark, minimum mercy!"""

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a hilarious and brutally honest code review AI."},
                {"role": "user", "content": roast_prompt}
            ],
            max_tokens=300,
            temperature=0.8
        )

      
        roast = response.choices[0].message.content.strip()
        
        return {
            "original_message": commit.message,
            "roast": roast
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def read_root():
    about="Welcome to the FastAPI with Google Generative AI!"
    licenses = {'Full Name':"Samuel Peters", 'socials':{'github':"https://github.com/Petsamuel", "repository":"https://github.com/Petsamuel/weather-crop-API", "LinkedIn":"https:linkedIn.com/in/bieefilled"}, 'year':"2024"}
    return {"message": about, "License":licenses }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=5000)