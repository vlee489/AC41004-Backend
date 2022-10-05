from pydantic import BaseModel, Field
from.resourceType import ResourceType


class Rule(BaseModel):
    """Rule's details"""
    id: str = Field(description="Rule's ID")
    name: str = Field(description="Rule's Name")
    resource_type: ResourceType = Field(description="Resource Type")
    description: str = Field(description="Description of rule")


class ResourceRule(Rule):
    compliant: bool = Field(description="If resource is compliant with rule")
    exception: bool = Field(description="If rule has exception applied", default=False)
