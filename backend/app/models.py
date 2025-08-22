from pydantic import BaseModel, EmailStr


class UserPublic(BaseModel):
    email: EmailStr


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
