"""Handled Customer profiles"""
from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Union
if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId
from bson.errors import InvalidId

from app.database.models import Customer


async def get_customer_by_id(self: 'DBConnector', customer_id: Union[ObjectId, str]) -> Optional[Customer]:
    """
    Get user via their email
    :param self:
    :param customer_id: Customer's ID
    :return:
    """
    try:
        # If ID is a string turn it into an ObjectID
        if type(customer_id) is str:
            customer_id = ObjectId(customer_id)
        if result := await self._db.customers.find_one({"_id": customer_id}):
            return Customer(result)
    except InvalidId:
        return None

