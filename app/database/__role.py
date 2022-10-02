"""Handles User Roles profiles"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId
from bson.errors import InvalidId

from app.database.models import UserRole


async def get_role_by_id(self: 'DBConnector', role_id: str) -> Optional[UserRole]:
    """
    Get role via ID
    :param self:
    :param role_id: Role's ID
    :return:
    """
    try:
        if result := await self._db.userRoles.find_one({"_id": ObjectId(role_id)}):
            return UserRole(result)
    except InvalidId:
        return None
