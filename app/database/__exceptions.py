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


async def get_exception_from_exception_id(self: 'DBConnector', exception_id: str) -> Optional[ExceptionPipeline]:
    """
    Get exceptions from exception ID
    :param self:
    :param exception_id: exception ID to get exceptions for
    :return: list of rule exceptions
    """
    try:
        return_list = []
        if type(exception_id) == str:
            exception_id = ObjectId(exception_id)
        exception_cursor = self._db.exceptions.aggregate([
            {
                '$match': {
                    '_id': exception_id
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
        if len(return_list) == 1:
            return return_list[0]
        else:
            raise IndexError("Too many responses")
    except InvalidId:
        return None


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


async def add_exception(
        self: 'DBConnector',
        customer_id: Union[ObjectId, str],
        rule_id: Union[ObjectId, str],
        last_updated_by: Union[ObjectId, str],
        exception_value: str,
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
    return (await self._db.exceptions.insert_one({
        "customer_id": customer_id,
        "rule_id": rule_id,
        "last_updated_by": last_updated_by,
        "exception_value": exception_value,
        "justification": justification,
        "review_date": review_date,
        "last_updated": last_updated
    })).inserted_id


async def update_exception(self: 'DBConnector', exception_id: Union[ObjectId, str],
                           last_updated_by: Union[ObjectId, str], last_updated: datetime,
                           exception_value: Optional[str], justification: Optional[str],
                           review_date: Optional[datetime]) -> bool:
    if type(exception_id) == str:
        exception_id = ObjectId(exception_id)
    if type(last_updated_by) == str:
        last_updated_by = ObjectId(last_updated_by)
    update = {
        "last_updated_by": last_updated_by,
        "last_updated": last_updated
    }
    if exception_value is not None:
        update["exception_value"] = exception_value
    if justification is not None:
        update["justification"] = justification
    if review_date is not None:
        update["review_date"] = review_date

    response = await self._db.exceptions.update_one({"_id": exception_id}, {"$set": update})
    return response.acknowledged
