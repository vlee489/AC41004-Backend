from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional, Union
if TYPE_CHECKING:
    from app.database import DBConnector
from bson import ObjectId


async def add_exception(
        self: 'DBConnector',
        customer_id: Union[ObjectId, str],
        rule_id: Union[ObjectId, str],
        last_updated_by: Union[ObjectId, str],
        exception_value: Union[ObjectId, str],
        justification: str,
        review_date: datetime,
        last_updated: datetime
    ) -> ObjectId:
    if type(customer_id) == str:
        customer_id = ObjectId(customer_id)
    if type(rule_id) == str:
        rule_id = ObjectId(rule_id)
    if type(last_updated_by) == str:
        last_updated_by = ObjectId(last_updated_by)
    if type(exception_value) == str:
        exception_value = ObjectId(exception_value)
    return (await self._db.exceptions.insert_one({
        "customer_id": customer_id,
        "rule_id": rule_id,
        "last_updated_by": last_updated_by,
        "exception_value": exception_value,
        "justification": justification,
        "review_date": review_date,
        "last_updated": last_updated
    })).inserted_id
