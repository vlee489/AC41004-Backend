"""Non-compliance DB Model"""
from dataclasses import dataclass, InitVar, field
from bson import objectid


@dataclass
class NonCompliance:
    init_data: InitVar[dict]
    resource_id: str = field(init=False, default="")
    rule_id: str = field(init=False, default="")

    def __post_init__(self, init_data: dict):
        self._resource_id = init_data.get("resource_id", "")
        self.resource_id = str(self._resource_id)

        self._rule_id = init_data.get("rule_id", "")
        self.rule_id = str(self._rule_id)



