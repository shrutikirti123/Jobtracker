from pydantic import BaseModel

# -------- USER SCHEMAS --------

class UserCreate(BaseModel):
    name: str
    email: str
    password: str


class UserResponse(BaseModel):
    id: int
    name: str
    role: str
    email: str

    class Config:
        from_attributes = True