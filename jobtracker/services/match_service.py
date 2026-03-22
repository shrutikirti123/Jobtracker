from services.resume_service import extract_skills


def extract_job_skills(job_description: str):

    job_description = job_description.lower()

    job_skills = []

    for skill in extract_skills(job_description):
        job_skills.append(skill)

    return job_skills


def calculate_match(resume_skills, job_skills):

    matching = []
    missing = []

    for skill in job_skills:
        if skill in resume_skills:
            matching.append(skill)
        else:
            missing.append(skill)

    if len(job_skills) == 0:
        score = 0
    else:
        score = int((len(matching) / len(job_skills)) * 100)

    return {
        "score": score,
        "matching_skills": matching,
        "missing_skills": missing
    }