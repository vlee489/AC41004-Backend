from pydantic import BaseModel, Field

from .customer import Customer
from .platform import Platform


class Account(BaseModel):
    id: str = Field(description="Account's ID")
    name: str = Field(descprition="Account's Name")
    reference: str = Field(descprition="Account's Reference")
    customer: Customer = Field(description="Customer account is with")
    platform: Platform = Field(description="Platform account is using")
