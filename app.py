import os
from fastapi import FastAPI
from pydantic import BaseModel
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class EmailInput(BaseModel):
    subject: str
    body: str

@app.post("/process-email")
def process_email(email: EmailInput):
    prompt = f"""
You are an AI email assistant.

Classify the email and generate a response.

Email:
Subject: {email.subject}
Body: {email.body}

Return JSON:
- category (client, spam, internal)
- priority (high, medium, low)
- reply (short professional reply)
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )

    return {"result": response.choices[0].message.content}
