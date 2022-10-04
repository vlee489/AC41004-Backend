from pydantic import BaseModel, Field
from .platform import Platform


class ResourceType(BaseModel):
    """Resource Type"""
    id: str = Field(description="Rule's ID")
    name: str = Field(description="Rule's Name")
    platform: Platform = Field(description="Platform rule part of")

