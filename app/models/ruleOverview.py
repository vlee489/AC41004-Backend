"""Model for Rule overview"""
from pydantic import BaseModel, Field
from typing import List
from .rule import Rule


class RuleOverview(BaseModel):
    rule: Rule = Field(description="Rule in question")
    non_compliant: List[str] = Field(description="List of ID for resources that are non-compliant")
    compliant: List[str] = Field(description="List of ID for resources that are compliant")
