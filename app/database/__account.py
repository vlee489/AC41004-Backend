"""Handles Accounts"""
from __future__ import annotations
from typing import TYPE_CHECKING, List, Union, Optional
if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId
from bson.errors import InvalidId

from app.database.models import Account


async def get_account_by_customer_id(self: 'DBConnector', customer_id: Union[ObjectId, str]) -> List[Account]:
    """
    Get Account with the Customer ID
    :param self:
    :param customer_id: Customer's ID
    :return: list of accounts for customer
    """
    accounts = []
    try:
        # If ID is a string turn it into an ObjectID
        if type(customer_id) is str:
            customer_id = ObjectId(customer_id)
        async for c in self._db.accounts.find({"customer_id": customer_id}):
            accounts.append(Account(c))
        return accounts
    except InvalidId:
        return []

