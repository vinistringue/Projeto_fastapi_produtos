from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: Optional[str] = "user"  # O papel default será "user"

class UserLogin(BaseModel):
    username: str
    password: str

class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        orm_mode = True
