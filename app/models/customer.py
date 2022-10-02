from pydantic import BaseModel, Field


class Customer(BaseModel):
    """Customer's details"""
    id: str = Field(description="Customer's ID")
    name: str = Field(description="Customer's Name")
