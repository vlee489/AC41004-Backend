from pydantic import BaseModel, Field


class Role(BaseModel):
    """User Role's details"""
    id: str = Field(description="Customer's ID")
    name: str = Field(description="Customer's Name")
    level: int = Field(description="Role's system access Level")
