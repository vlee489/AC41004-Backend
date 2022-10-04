from pydantic import BaseModel, Field
from.resourceType import ResourceType


class Rule(BaseModel):
    """Rule's details"""
    id: str = Field(description="Rule's ID")
    name: str = Field(description="Rule's Name")
    resource_type: ResourceType = Field(description="Resource Type")

