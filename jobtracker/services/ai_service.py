from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_resume_match(resume_skills, job_description):

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a career assistant."},
                {"role": "user", "content": f"""
Resume skills: {resume_skills}

Job description: {job_description}

Explain why this job matches the resume.
"""}
            ]
        )

        return response.choices[0].message.content

    except Exception:
        return "AI analysis unavailable. Showing skill match only."