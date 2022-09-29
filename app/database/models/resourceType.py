"""Resource Type DB Model"""
from dataclasses import dataclass, field

from .base import Base


@dataclass
class ResourceType(Base):
    platform_id: str = field(init=False, default="")

    def __post_init__(self, init_data: dict):
        super().__post_init__(init_data)

        self._platform_id = init_data.get("platform_id", "")
        self.platform_id = str(self._platform_id)
