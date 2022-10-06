"""Non-compliance Audit DB Model"""
from dataclasses import dataclass, InitVar, field
from datetime import datetime
from bson import objectid


@dataclass
class NonComplianceAudit:
    init_data: InitVar[dict]
    id: str = field(init=False, default="")
    resource_id: str = field(init=False, default="")
    rule_id: str = field(init=False, default="")
    user_id: str = field(init=False, default="")
    action: str = field(init=False, default="")
    action_datetime: datetime = field(init=False)

    def __post_init__(self, init_data: dict):
        self._id = init_data.get("_id", "")
        self.id = str(self._id)

        self._resource_id = init_data.get("resource_id", "")
        self.resource_id = str(self._resource_id)

        self._user_id = init_data.get("user_id", "")
        self.user_id = str(self._user_id)

        self._customer_id = init_data.get("customer_id", "")
        self.customer_id = str(self._customer_id)

        self._rule_id = init_data.get("rule_id", "")
        self.rule_id = str(self._rule_id)

        self.action = init_data.get("action")
        self.action_datetime = init_data.get("action_datetime")

    @property
    def object_id(self) -> objectid.ObjectId:
        """
        Get base's objectID
        :return:
        """
        return self._id

