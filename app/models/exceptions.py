from pydantic import BaseModel, Field
from datetime import datetime

from .customer import Customer
from .rule import Rule
from .user import ExceptionUser
from .resources import ExceptionResource


class RuleException(BaseModel):
    id: str = Field(description="Exception's ID")
    customer: Customer = Field(description="Customer Exception belong to")
    rule: Rule = Field(description="Rule the exception is for")
    last_updated_by: ExceptionUser = Field(description="Exception was last updated by")
    exception_value: str
    justification: str = Field(description="Justification for exception")
    review_date: datetime = Field(description="when the review date is")
    last_updated: datetime = Field(description="when the exception was last updated")


class AccountRuleException(RuleException):
    resource: ExceptionResource = Field(description="Resource exception tied to")
