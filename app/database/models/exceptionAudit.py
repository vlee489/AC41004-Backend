from dataclasses import dataclass, InitVar, field
from bson import objectid
from datetime import datetime
from typing import Optional


@dataclass
class ExceptionAudit:
    init_data: InitVar[dict]
    id: str = field(init=False, default="")
    exception_id: str = field(init=False, default="")
    user_id: str = field(init=False, default="")
    customer_id: str = field(init=False, default="")
    rule_id: str = field(init=False, default="")

    action: str = field(init=False, default="")
    action_datetime: datetime = field(init=False)

    old_value: Optional[str] = field(init=False, default=None)
    new_value: Optional[str] = field(init=False, default=None)

    old_justification: Optional[str] = field(init=False, default=None)
    new_justification: Optional[str] = field(init=False, default=None)

    old_review_date: Optional[datetime] = field(init=False, default=None)
    new_review_date: Optional[datetime] = field(init=False, default=None)

    def __post_init__(self, init_data: dict):
        self._id = init_data.get("_id", "")
        self.id = str(self._id)

        self._user_id = init_data.get("user_id", "")
        self.user_id = str(self._user_id)

        self._exception_id = init_data.get("exception_id", "")
        self.exception_id = str(self._exception_id)

        self._customer_id = init_data.get("customer_id", "")
        self.customer_id = str(self._customer_id)

        self._rule_id = init_data.get("rule_id", "")
        self.rule_id = str(self._rule_id)

        self.action = init_data.get("action")
        self.action_datetime = init_data.get("action_dt")

        self.old_value = init_data.get("old_value", None)
        self.new_value = init_data.get("new_value", None)
        self.old_justification = init_data.get("old_justification", None)
        self.new_justification = init_data.get("new_justification", None)
        self.old_review_date = init_data.get("old_review_date", None)
        self.new_review_date = init_data.get("new_review_date", None)

    @property
    def object_id(self) -> objectid.ObjectId:
        """
        Get base's objectID
        :return:
        """
        return self._id
