from dataclasses import dataclass, InitVar, field
from bson import objectid
from datetime import datetime
from typing import Optional


@dataclass
class ExceptionAudit:
    init_data: InitVar[dict]
    id: str = field(init=False, default="")
    user_id: str = field(init=False, default="")
    customer_id: str = field(init=False, default="")
    rule_id: str = field(init=False, default="")

    action: str = field(init=False, default="")
    action_datetime: datetime = field(init=False)

    old_value: Optional[str] = field(init=False, default="")
    new_value: Optional[str] = field(init=False, default="")

    old_justification: Optional[str] = field(init=False, default="")
    new_justification: Optional[str] = field(init=False, default="")

    old_review_date: Optional[datetime] = field(init=False)
    new_review_date: Optional[datetime] = field(init=False)

    def __post_init__(self, init_data: dict):
        self._id = init_data.get("_id", "")
        self.id = str(self._id)

        self._user_id = init_data.get("user_id", "")
        self.user_id = str(self._user_id)

        self._customer_id = init_data.get("customer_id", "")
        self.customer_id = str(self._customer_id)

        self._rule_id = init_data.get("rule_id", "")
        self.rule_id = str(self._rule_id)

        self.action = init_data.get("action")
        self.action_datetime = init_data.get("action_datetime")

        if ("old_value" in init_data) and ("new_value" in init_data):
            self.old_value = init_data.get("old_value")
            self.new_value = init_data.get("new_value")

        if ("old_justification" in init_data) and ("new_justification" in init_data):
            self.old_justification = init_data.get("old_justification")
            self.new_justification = init_data.get("new_justification")

        if ("old_review_date" in init_data) and ("new_review_date" in init_data):
            self.old_review_date = init_data.get("old_review_date")
            self.new_review_date = init_data.get("new_value")

    @property
    def object_id(self) -> objectid.ObjectId:
        """
        Get base's objectID
        :return:
        """
        return self._id
