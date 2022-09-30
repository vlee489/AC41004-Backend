"""Session Login request/response model"""
from pydantic import BaseModel, Field, EmailStr
from typing import Optional


class LoginCredentials(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)


class LoginResponse(BaseModel):
    status: bool = Field(description="status of login attempt")


class LogoutResponse(BaseModel):
    status: bool = Field(description="status of logout attempt")
