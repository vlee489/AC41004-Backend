"""Handles Rule Exceptions"""
from __future__ import annotations
from typing import TYPE_CHECKING, List, Union, Optional

if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId
from bson.errors import InvalidId

from app.database.models import ExceptionPipeline


async def get_exception_from_exception_value(self: 'DBConnector', exception_value: str) -> List[ExceptionPipeline]:
    """
    Get exceptions from exception value
    :param self:
    :param exception_value: exception value to get exceptions for
    :return: list of rule exceptions
    """
    return_list = []
    exception_cursor = self._db.exceptions.aggregate([
        {
            '$match': {
                'exception_value': f"{exception_value}"
            }
        }, {
            '$lookup': {
                'from': 'rules',
                'localField': 'rule_id',
                'foreignField': '_id',
                'as': 'rule'
            }
        }, {
            '$unwind': {
                'path': '$rule'
            }
        }, {
            '$lookup': {
                'from': 'resourceTypes',
                'localField': 'rule.type_id',
                'foreignField': '_id',
                'as': 'rule.resource_type'
            }
        }, {
            '$unwind': {
                'path': '$rule.resource_type'
            }
        }, {
            '$lookup': {
                'from': 'platforms',
                'localField': 'rule.resource_type.platform_id',
                'foreignField': '_id',
                'as': 'rule.resource_type.platform'
            }
        }, {
            '$unwind': {
                'path': '$rule.resource_type.platform'
            }
        }, {
            '$lookup': {
                'from': 'customers',
                'localField': 'customer_id',
                'foreignField': '_id',
                'as': 'customer'
            }
        }, {
            '$unwind': {
                'path': '$customer'
            }
        }, {
            '$lookup': {
                'from': 'users',
                'localField': 'last_updated_by',
                'foreignField': '_id',
                'as': 'last_updated_by_user'
            }
        }, {
            '$unwind': {
                'path': '$last_updated_by_user'
            }
        }
    ])
    async for rule_exception in exception_cursor:
        return_list.append(ExceptionPipeline(rule_exception, self._db))
    return return_list
