"""User Role DB Model"""
from dataclasses import dataclass, field

from .base import Base


@dataclass
class UserRole(Base):
    # 0 Compliance Audit
    # 1 Compliance Manager
    # 2 System Admin
    level: int = field(init=False, default=0)

    def __post_init__(self, init_data: dict):
        super().__post_init__(init_data)
        self.level = init_data.get("level", 0)
