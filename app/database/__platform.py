"""Handles Platforms"""
from __future__ import annotations
from typing import TYPE_CHECKING, List, Union, Optional
if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId
from bson.errors import InvalidId

from app.database.models import Platform


async def get_platform_by_id(self: 'DBConnector', platform_id: Union[ObjectId, str]) -> Optional[Platform]:
    """
    Get Platform by ID
    :param self:
    :param platform_id: Platform's ID
    :return: Platform's info
    """
    try:
        # If ID is a string turn it into an ObjectID
        if type(platform_id) is str:
            platform_id = ObjectId(platform_id)
        if result := await self._db.platforms.find_one({"_id": platform_id}):
            return Platform(result)
    except InvalidId:
        return None

