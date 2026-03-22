# Jobtracker
AI Job Tracker is a full-stack platform for tracking job applications, analyzing resumes, and discovering relevant opportunities using skill-based matching. It uses FastAPI, PostgreSQL, Redis, and Celery with caching, background workers, authentication, pagination, rate limiting, and logging. A React frontend and cloud deployment are planned.
The system combines a modern backend architecture with cloud-ready infrastructure to simulate a production-grade job tracking platform.

---

## Core Features

### User Management
- Secure user authentication using JWT
- User-specific job tracking and dashboards

### Job Tracking
- Create, update, delete, and manage job applications
- Track application status (Applied, Saved, Interviewing, Rejected)

### Resume Intelligence
- Upload resume (PDF)
- Automatic skill extraction from resume
- Resume analysis and skill detection

### Job Matching
- Match resume skills with job descriptions
- Calculate match score
- Identify missing and matching skills

### External Job Search
- Fetch real remote jobs from Remotive API
- Automatically match them with resume skills
- Rank jobs based on match score

### Performance Optimization
- Redis caching for job searches
- Background resume processing using Celery workers
- API rate limiting

### Advanced API Features
- Pagination
- Filtering
- Logging
- Error handling
- Database migrations with Alembic

---

## Tech Stack

### Backend
- FastAPI
- Python 3.11
- SQLAlchemy ORM
- Pydantic
- JWT Authentication

### Database
- PostgreSQL

### Infrastructure & Performance
- Redis
- Celery
- Docker
- Docker Compose
- Alembic

### External Integrations
- Remotive Job API

---

## Planned Full System Architecture


User
↓
Frontend Dashboard (React / Next.js)
↓
FastAPI Backend
↓
JWT Authentication
↓
PostgreSQL Database
↓
Redis Cache
↓
Celery Workers
↓
External Job APIs


---

## API Endpoints

### Authentication
POST /auth/signup  
POST /auth/login  

### Jobs
POST /jobs  
GET /jobs  
GET /jobs/{job_id}/match  
GET /jobs/recommendations  

### Resume
POST /resume/upload  
GET /resume/skills  

### Job Discovery
GET /jobs/search  
GET /jobs/search-match  
POST /jobs/save-external  

---

## Example Job Matching Response


{
"title": "Backend Engineer",
"company": "Stripe",
"match_score": 86,
"matching_skills": ["python", "docker", "postgresql"],
"missing_skills": ["kubernetes"]
}


---

## Local Setup

Clone repository


git clone https://github.com/yourusername/jobtracker-ai.git


Install dependencies


pip install -r requirements.txt


Run FastAPI server


uvicorn main:app --reload


Run Celery worker


celery -A core.celery_app.celery worker --pool=solo --loglevel=info


Run Docker services


docker compose up


---

## Future Improvements

- AI based semantic skill matching
- Resume embeddings and vector search
- Full React dashboard
- Cloud deployment (Render / AWS)
- Job recommendation engine
- Analytics dashboard
- Email alerts for job matches

---

## Author

Shruti  
Cloud & DevOps / Backend Engineering Enthusiast
