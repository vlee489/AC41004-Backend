from pydantic import BaseModel, Field
from datetime import datetime

from .account import Account
from .resourceType import ResourceType


class Resource(BaseModel):
    """Resource's details"""
    reference: str = Field("Resource platform reference")
    account: Account = Field("Account resource is tied to")
    resource_type: ResourceType = Field(description="resource's type")
    last_updated: datetime = Field(description="Time resource was last updated")
    metadata: dict = Field(description="Resource's metadata")

