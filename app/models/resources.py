from pydantic import BaseModel, Field
from datetime import datetime

from .account import Account
from .resourceType import ResourceType


class Resource(BaseModel):
    """Resource's details"""
    id: str = Field(description="Resource's ID")
    name: str = Field(description="Resource's Name")
    reference: str = Field("Resource platform reference")
    account: Account = Field("Account resource is tied to")
    resource_type: ResourceType = Field(description="resource's type")
    last_updated: datetime = Field(description="Time resource was last updated")
    metadata: dict = Field(description="Resource's metadata")


class ExceptionResource(BaseModel):
    """Resource's details for exceptions"""
    id: str = Field(description="Resource's ID")
    name: str = Field(description="Resource's Name")
    reference: str = Field("Resource platform reference")
    resource_type: ResourceType = Field(description="resource's type")
    last_updated: datetime = Field(description="Time resource was last updated")
    metadata: dict = Field(description="Resource's metadata")


class SearchResource(BaseModel):
    """resource search result"""
    id: str = Field(description="Resource's ID")
    name: str = Field(description="Resource's Name")
    reference: str = Field("Resource platform reference")
    last_updated: datetime = Field(description="Time resource was last updated")
    score: float = Field(description="Search Score")
