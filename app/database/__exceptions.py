"""Handles Rule Exceptions"""
from __future__ import annotations
from typing import TYPE_CHECKING, List, Union, Optional
from datetime import datetime

if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId
from bson.errors import InvalidId

from app.database.models import ExceptionPipeline, AccountExceptionPipeline


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


async def get_exception_by_date_account_id(self: 'DBConnector', account_id: Union[str, ObjectId],
                                           start_period: Union[datetime, None] = None,
                                           end_period: Union[datetime, None] = None) -> List[AccountExceptionPipeline]:
    """
    Get exceptions by account ID and time period
    :param self:
    :param account_id: Account's ID
    :param start_period: Start period of review date
    :param end_period: End period of review date
    :return: list of rule exceptions
    """
    # If ID is a string turn it into an ObjectID
    try:
        return_list = []
        if type(account_id) is str:
            account_id = ObjectId(account_id)
        date_period = {}
        if start_period:
            date_period["$gte"] = start_period
        if end_period:
            date_period["$lt"] = end_period
        if date_period:
            date_period = {'review_date': date_period}
        exception_cursor = self._db.exceptions.aggregate([
            {
                '$match': date_period
            }, {
                '$lookup': {
                    'from': 'resources',
                    'localField': 'exception_value',
                    'foreignField': 'reference',
                    'as': 'resource'
                }
            }, {
                '$unwind': {
                    'path': '$resource'
                }
            }, {
                '$match': {
                    'resource.account_id': account_id
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
            return_list.append(AccountExceptionPipeline(rule_exception, self._db))
        return return_list
    except InvalidId:
        return []