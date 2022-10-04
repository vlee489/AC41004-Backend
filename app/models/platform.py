from pydantic import BaseModel, Field


class Platform(BaseModel):
    """Customer's details"""
    id: str = Field(description="Platform's ID")
    name: str = Field(description="Name's Name")
