"""Handles Rules"""
from __future__ import annotations
from typing import TYPE_CHECKING, List, Union, Optional
if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId
from bson.errors import InvalidId

from app.database.models import Rule


async def get_rule_by_id(self: 'DBConnector', rule_id: Union[ObjectId, str]) -> Optional[Rule]:
    """
    Get rule by ID
    :param self:
    :param rule_id: Rule's ID
    :return: Rule's info
    """
    try:
        # If ID is a string turn it into an ObjectID
        if type(rule_id) is str:
            rule_id = ObjectId(rule_id)
        if result := await self._db.rules.find_one({"_id": rule_id}):
            return Rule(result)
    except InvalidId:
        return None

