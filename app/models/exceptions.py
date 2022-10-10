from typing import Optional

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
    exception_value: str = Field("Exception's value")
    justification: str = Field(description="Justification for exception")
    review_date: datetime = Field(description="When the review date is")
    last_updated: datetime = Field(description="When the exception was last updated")
    suspended: bool = Field(description="Whether the exception is suspended")


class AccountRuleException(RuleException):
    resource: ExceptionResource = Field(description="Resource exception tied to")


class AddExceptionRequest(BaseModel):
    resource_id: str = Field(description="Resource's id")
    rule_id: str = Field(description="Rule's id")
    justification: str = Field(description="Exception's justification")
    review_date: datetime = Field(description="Exception's next review datetime")


class EditExceptionRequest(BaseModel):
    exception_value: Optional[str] = Field(description="Exception's value", default=None)
    justification: Optional[str] = Field(description="Exception's justification", default=None)
    review_date: Optional[datetime] = Field(description="Exception's next review datetime", default=None)
    suspended: Optional[bool] = Field(description="Whether the exception is suspended")
