from datetime import datetime
from pydantic import Field, BaseModel

from .resources import Resource
from .rule import Rule
from .user import ExceptionUser


class NonComplianceAudit(BaseModel):
    id: str = Field(description="Non-compliance audit's ID")
    resource: Resource = Field(description="Resource")
    rule: Rule = Field(description="Rule")
    user: ExceptionUser = Field(description="User's ID")
    action: str = Field(description="Action's ID")
    action_datetime: datetime = Field(description="Action's datetime")
