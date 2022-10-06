from datetime import datetime
from pydantic import Field, BaseModel


class NonComplianceAudit(BaseModel):
    id: str = Field(description="Non-compliance audit's ID")
    resource_id: str = Field(description="Resource's ID")
    rule_id: str = Field(description="Rule's ID")
    user_id: str = Field(description="User's ID")
    action: str = Field(description="Action's ID")
    action_datetime: datetime = Field(description="Action's datetime")
