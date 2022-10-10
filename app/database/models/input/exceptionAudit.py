"""Exception Audit input model class"""
from dataclasses import dataclass, InitVar, field
from typing import Optional, List
from datetime import datetime
import copy
from bson import ObjectId
from bson.errors import InvalidId

from app.database.models import RuleException


@dataclass
class NewExceptionAudit:
    rule_exception: RuleException
    user_id: str
    new_value: Optional[str] = field(default=None)
    new_justification: Optional[str] = field(default=None)
    new_review_date: Optional[datetime] = field(default=None)
    action_datetime: datetime = field(init=False)
    action: str = field(init=False, default="add_exception")

    def __post_init__(self):
        self.action_datetime = datetime.utcnow()

    @property
    def insert_dict(self) -> dict:
        try:
            insert_dict = {
                "exception_id": self.rule_exception.object_id,
                "user_id": ObjectId(self.user_id),
                "customer_id": ObjectId(self.rule_exception.customer_id),
                "rule_id": ObjectId(self.rule_exception.rule_id),
                "action": self.action,
                "action_dt": self.action_datetime,
                "new_value": self.new_value,
                "new_justification": self.new_justification,
                "new_review_date": self.new_review_date,
            }
            return insert_dict
        except InvalidId:
            pass


@dataclass
class UpdateExceptionAudit:
    rule_exception: RuleException
    user_id: str
    action_datetime: datetime = field(init=False)

    new_value: Optional[str] = field(default=None)
    new_justification: Optional[str] = field(default=None)
    new_review_date: Optional[datetime] = field(default=None)

    def __post_init__(self):
        self.action_datetime = datetime.utcnow()

    def new_audit(self) -> List[dict]:
        """
        Returns a list of new dicts that should be inserted for audit updates
        :return:
        """
        new_audit = []
        try:
            base_dict = {
                    "exception_id": self.rule_exception.object_id,
                    "user_id": ObjectId(self.user_id),
                    "customer_id": ObjectId(self.rule_exception.customer_id),
                    "rule_id": ObjectId(self.rule_exception.rule_id),
                }
            if self.new_value:
                new_audit.append(dict({
                    "action": "update_value",
                    "action_dt": self.action_datetime,
                    "new_value": self.new_value,
                    "old_value": self.rule_exception.exception_value,
                }, **base_dict))
            if self.new_justification:
                new_audit.append(dict({
                    "action": "update_justification",
                    "action_dt": self.action_datetime,
                    "new_justification": self.new_justification,
                    "old_justification": self.rule_exception.justification,
                }, **base_dict))
            if self.new_review_date:
                new_audit.append(dict({
                    "action": "update_justification",
                    "action_dt": self.action_datetime,
                    "new_review_date": self.new_review_date,
                    "old_review_date": self.rule_exception.review_date,
                }, **base_dict))
        except InvalidId:
            pass
        return new_audit
