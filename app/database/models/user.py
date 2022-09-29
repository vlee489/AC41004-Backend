"""User DB Model"""
from dataclasses import dataclass, InitVar, field
from typing import List


@dataclass
class User:
    """User DB Model"""
    user_data: InitVar[dict]
    id: str = field(init=False, default="")
    email: str = field(init=False, default="")
    password_hash: bytes = field(init=False, default=b"")
    first_name: str = field(init=False, default="")
    last_name: str = field(init=False, default="")
    companies: List[str] = field(init=False, default_factory=list)

    def __post_init__(self, user_data: dict):
        self._id = user_data.get("_id", "")
        self.id = str(self._id)

        self.email = user_data.get("discord_id", "")
        self.password_hash = user_data.get("sso_id", b"")
        self.first_name = user_data.get("avatar", "")
        self.last_name = user_data.get("discord_username", "")
        self.companies = user_data.get("last_session", [])
