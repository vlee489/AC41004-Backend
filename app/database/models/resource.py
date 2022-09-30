"""Resource DB Model"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from .base import Base


@dataclass
class Resource(Base):
    reference: str = field(init=False, default="")
    account_id: str = field(init=False, default="")
    resource_type_id: str = field(init=False, default="")
    last_update: Optional[datetime] = field(init=False, default=None)
    metadata: dict = field(init=False, default_factory=dict)

    def __post_init__(self, init_data: dict):
        super().__post_init__(init_data)
        self.reference = init_data.get("resource_type_id", "")
        self.last_updated = init_data.get("resource_type_id", None)
        self.metadata = init_data.get("metadata", {})

        self._resource_type_id = init_data.get("resource_type_id", "")
        self.resource_type_id = str(self._resource_type_id)

        self._account_id = init_data.get("account_id", "")
        self.account_id = str(self._account_id)


