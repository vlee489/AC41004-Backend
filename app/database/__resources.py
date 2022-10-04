"""Handles Resources"""
from __future__ import annotations
from typing import TYPE_CHECKING, List, Union, Optional
if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId
from bson.errors import InvalidId

from app.database.models import Resource


async def get_resource_by_id(self: 'DBConnector', resource_id: Union[ObjectId, str]) -> Optional[Resource]:
    """
    Get Resource by ID
    :param self:
    :param resource_id: Resource's ID
    :return:
    """
    try:
        # If ID is a string turn it into an ObjectID
        if type(resource_id) is str:
            resource_id = ObjectId(resource_id)
        if document := self._db.resources.find_one({"_id": resource_id}):
            return Resource(document)
    except InvalidId:
        return None


async def get_resources_by_account_id(self: 'DBConnector', account_id: Union[ObjectId, str]) -> List[Resource]:
    """
    Get Resources with the Account ID
    :param self:
    :param account_id: Account's ID
    :return: list of resources for account
    """
    resources = []
    try:
        # If ID is a string turn it into an ObjectID
        if type(account_id) is str:
            account_id = ObjectId(account_id)
        async for r in self._db.resources.find({"account_id": account_id}):
            resources.append(Resource(r))
        return resources
    except InvalidId:
        return []


