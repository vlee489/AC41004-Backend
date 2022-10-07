from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AddExceptionRequest(BaseModel):
    resource_id: str = Field(description="Resource's id")
    rule_id: str = Field(description="Rule's id")
    exception_value: str = Field(description="Exception's value")
    justification: str = Field(description="Exception's justification")
    review_date: datetime = Field(description="Exception's next review datetime")


class EditExceptionRequest(BaseModel):
    resource_id: str = Field(description="Resource's id")
    rule_id: str = Field(description="Rule's id")
    exception_value: Optional[str] = Field(description="Exception's value")
    justification: Optional[str] = Field(description="Exception's justification")
    review_date: Optional[datetime] = Field(description="Exception's next review datetime")