from typing import List, Optional
from pydantic import BaseModel, EmailStr
from models.events import Event


class User(BaseModel):
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
