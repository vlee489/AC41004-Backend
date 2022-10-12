from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum
from typing import Optional

from .user import ExceptionUser
from .customer import Customer
from .rule import Rule


class ValidActions(str, Enum):
    update_value: "update_value"
    update_justification: "update_justification"
    update_review_date: "update_review_date"
    add_exception: "add_exception"
    remove_exception: "remove_exception"


class ExceptionAudit(BaseModel):
    id: str = Field(description="exception audit's ID")
    user: ExceptionUser = Field(description="User who preformed change")
    customer: Customer = Field(description="Customer exception audit is for")
    rule: Rule = Field(description="Rule exception applies to")
    action: str = Field(description="action that occurred")
    action_datetime: datetime = Field(description="when the action occurred")

    old_value: Optional[str] = Field(description="Old exception value")
    new_value: Optional[str] = Field(description="New exception value")
    old_justification: Optional[str] = Field(description="old justification")
    new_justification: Optional[str] = Field(description="new justification")
    old_review_date: Optional[datetime] = Field(description="Old review date")
    new_review_date: Optional[datetime] = Field(description="new review date")
    old_suspended: Optional[bool] = Field(description="Old suspended date")
    new_suspended: Optional[bool] = Field(description="new suspended date")





