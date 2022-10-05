"""Handles Non Compliance"""
from __future__ import annotations
from typing import TYPE_CHECKING, List, Union, Optional

if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId
from bson.errors import InvalidId

from app.database.models import NonCompliance


async def get_non_complaince_by_resource_id(self: 'DBConnector', resource_id: Union[ObjectId, str]) ->\
        List[NonCompliance]:
    """
    Get Non Compliance from resource_id
    :param self:
    :param resource_id: Resource's ID
    :return: List of Non Compliance
    """
    return_list = []
    try:
        # If ID is a string turn it into an ObjectID
        if type(resource_id) is str:
            resource_id = ObjectId(resource_id)
        async for document in self._db.nonCompliances.find({"resource_id": resource_id}):
            return_list.append(NonCompliance(document))
        return return_list
    except InvalidId:
        return return_list


async def get_non_complaince_by_rule_id(self: 'DBConnector', rule_id: Union[ObjectId, str]) ->\
        List[NonCompliance]:
    """
    Get Non Compliance from rule_id
    :param self:
    :param rule_id: Rule's ID
    :return: List of Non Compliance
    """
    return_list = []
    try:
        # If ID is a string turn it into an ObjectID
        if type(rule_id) is str:
            rule_id = ObjectId(rule_id)
        async for document in await self._db.nonCompliances.find({"rule_id": rule_id}):
            return_list.append(NonCompliance(document))
        return return_list
    except InvalidId:
        return return_list
