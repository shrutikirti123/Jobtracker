from pydantic import BaseModel

# -------- JOB SCHEMAS --------
class JobCreate(BaseModel):
    title: str
    company: str
    status: str
    description: str


class JobResponse(JobCreate):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class ExternalJobSave(BaseModel):
    title: str
    company: str
    description: str
    url: str | None = None