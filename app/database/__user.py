"""Handled User profiles"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from .__init__ import DBConnector

from app.database.models import User


async def get_user_via_email(self: 'DBConnector', email: str) -> Optional[User]:
    """
    Get user via their email
    :param self:
    :param email: User's email address
    :return:
    """
    if result := await self._db.users.find_one({"email": f"{email}"}):
        return User(result, self._db)

