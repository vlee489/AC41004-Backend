from pydantic import BaseModel, Field


class ResourceCountOverview(BaseModel):
    compliant: int = Field(description="Number of resources that are compliant")
    non_compliant: int = Field(description="Number of resources that are non-compliant")
