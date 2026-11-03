import json
from dotenv import load_dotenv
from openai import OpenAI
import os


load_dotenv()
client = OpenAI(
    base_url = "https://api.groq.com/openai/v1",
    api_key = os.getenv("GROQ_API_KEY"),
)

def extract_profile(cv_text: str) -> dict:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        response_format={"type": "json_object"},
        messages=[
            {
                "role": "system",
                "content": (
                    "Extract info from this CV. Return JSON with keys: "
                    "full_name, email, skills, experience, education. "
                    "Each value is a plain string. Use empty string if missing. "
                
                ),
            },
        {"role": "user", "content": cv_text},
        ],
    )
    return json.loads(response.choices[0].message.content)