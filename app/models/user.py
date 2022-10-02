from pydantic import BaseModel, Field, EmailStr


class UserProfile(BaseModel):
    """User Profile"""
    id: str = Field(description="User's ID")
    email: EmailStr = Field(description="User's email")
    first_name: str = Field(description="User's First Name")
    last_name: str = Field(description="User's Last Name")
    session_expiry: str = Field(description="Session expiry in ISO8601 from UTC")

    class Config:
        schema_extra = {
            "example": {
                "id": "6336e3470bb7de25d225190b",
                "email": "test@test.co.uk",
                "first_name": "Bob",
                "last_name": "blogs",
                "session_expiry": "2015-11-27T00:29:06.839600-05:00"
            }
        }
