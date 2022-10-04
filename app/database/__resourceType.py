"""Handles Resources Types"""
from __future__ import annotations
from typing import TYPE_CHECKING, List, Union, Optional
if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId
from bson.errors import InvalidId

from app.database.models import ResourceType


async def get_resource_type_by_id(self: 'DBConnector', resource_type_id: Union[ObjectId, str]) -> Optional[ResourceType]:
    """
    Get Resource Type by ID
    :param self:
    :param resource_type_id: Resource Type's ID
    :return:
    """
    try:
        # If ID is a string turn it into an ObjectID
        if type(resource_type_id) is str:
            resource_type_id = ObjectId(resource_type_id)
        if document := await self._db.resourceTypes.find_one({"_id": resource_type_id}):
            return ResourceType(document)
    except InvalidId:
        return None
