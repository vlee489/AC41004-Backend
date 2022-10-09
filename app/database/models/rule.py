"""Rule DB Model"""
from dataclasses import dataclass, field

from .base import Base


@dataclass
class Rule(Base):
    resource_type_id: str = field(init=False, default="")
    description: str = field(init=False, default="")

    def __post_init__(self, init_data: dict):
        super().__post_init__(init_data)
        self._resource_type_object_id = init_data.get("type_id", "")
        self.resource_type_id = str(self._resource_type_object_id)
        self.description = init_data.get("description", "")

