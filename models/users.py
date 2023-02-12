from typing import List, Optional
from sqlmodel import SQLModel, Field
from pydantic import BaseModel, EmailStr
from models.events import Event


class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: EmailStr = Field(index=True)
    password: str

    class Config:
        schema_extra = {
            "example": {
                "email": "user@gmail.com",
                'password': 'strong!'

            }
        }


class UserResponse(SQLModel):
    id: int
    email: EmailStr


class UserSignIn(BaseModel):
    email: EmailStr
    password: str
    events: Optional[List[Event]]

    class Config:
        schema_extra = {
            "example": {
                "email": "user@gmail.com",
                'password': 'strong!',
                'event': []
            }
        }


class TokenResponse(BaseModel):
    access_token: str
    token_type: str
