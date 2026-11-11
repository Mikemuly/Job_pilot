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


def explain_match(skills: str, experience: str, job_title: str, job_description: str) ->str:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You compare a candidate to a job. In 3 short sentences:"
                    "Why they fir, then what is missing. Plain text. no markdown."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"candidate skills: {skills}\n"
                    f"candidate experience: {experience}\n\n"
                    f"Job: {job_title}\n"
                    f"{job_description[:3000]}"
                ),
            },
        ],
    )
    return response.choices[0].message.content

def write_cover_letter(
        full_name: str,
        skills: str,
        experience: str,
        education: str,
        job_title: str,
        company: str,
        job_description: str,
) -> str:
    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content":(
                    "Write a concise cover letter, under 200 words, in plain text. "
                    "Use only facts from the candidate details. Never invent "
                    "experience, employers, or numbers. Sign off with the candidate's name."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Candidate: {full_name}\n"
                    f"Skills: {skills}\n"
                    f"Experience: {experience}\n"
                    f"Education: {education}\n\n"
                    f"Job: {job_title} at {company}\n"
                    f"{job_description[:3000]}"
                ),
            },
        ],
    )
    return response.choices[0].message.content
