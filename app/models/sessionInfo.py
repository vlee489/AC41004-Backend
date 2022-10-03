from pydantic import BaseModel, Field
from typing import Optional

from .role import Role
from .customer import Customer


class UserPermissions(BaseModel):
    """The Customer and Role logged-in user has"""
    role: Optional[Role] = Field(description="User's role", default=None)
    customer: Optional[Customer] = Field(description="Customer user is part of", default=None)
