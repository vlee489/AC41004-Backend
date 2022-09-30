from dataclasses import dataclass, InitVar, field
from bson import objectid
from datetime import datetime
from typing import Optional


@dataclass
class RuleException:
    init_data: InitVar[dict]
    id: str = field(init=False, default="")
    rule_id: str = field(init=False, default="")
    last_updated_by: str = field(init=False, default="")
    exception_value: str = field(init=False, default="")
    justification: str = field(init=False, default="")
    review_date: Optional[datetime] = field(init=False)
    last_updated: Optional[datetime] = field(init=False)

    name: str = field(init=False, default="")

    def __post_init__(self, init_data: dict):
        self._id = init_data.get("_id", "")
        self.id = str(self._id)

        self._rule_id = init_data.get("rule_id", "")
        self.rule_id = str(self._rule_id)

        self._last_updated_by = init_data.get("last_updated_by", "")
        self.last_updated_by = str(self._last_updated_by)

        self.exception_value = init_data.get("exception_value", "")
        self.justification = init_data.get("justification", "")
        self.review_date = init_data.get("review_date", None)
        self.last_updated = init_data.get("last_updated", None)

    @property
    def object_id(self) -> objectid.ObjectId:
        """
        Get base's objectID
        :return:
        """
        return self._id
