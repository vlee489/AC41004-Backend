"""Rule DB Model"""
from dataclasses import dataclass, field

from .base import Base


@dataclass
class Rule(Base):
    resource_type_id: str = field(init=False, default="")

    def __post_init__(self, init_data: dict):
        super().__post_init__(init_data)
        self.resource_type_id = init_data.get("type_id", "")

