import pdfplumber

SKILLS_DB = [
    "python",
    "java",
    "c++",
    "fastapi",
    "django",
    "flask",
    "docker",
    "kubernetes",
    "postgresql",
    "mysql",
    "mongodb",
    "redis",
    "aws",
    "azure",
    "gcp",
    "linux",
    "git",
    "terraform",
    "kafka",
    "react",
    "node",
    "typescript"
]

def extract_resume_text(file_path: str) -> str:
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""

    return text


def extract_skills(text: str):

    text = text.lower()
    detected_skills = []

    for skill in SKILLS_DB:
        if skill in text:
            detected_skills.append(skill)

    return detected_skills