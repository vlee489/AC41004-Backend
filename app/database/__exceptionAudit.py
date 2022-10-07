"""Handles Rule Exceptions"""
from __future__ import annotations
from typing import TYPE_CHECKING, List, Union, Optional
from datetime import datetime

if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId
from bson.errors import InvalidId

from app.database.models import ExceptionAuditPipeline


async def get_exception_audit_by_exception_id(self: 'DBConnector', exception_id: Union[str, ObjectId], ) -> \
        List[ExceptionAuditPipeline]:
    """
    Get exceptions audi by resource ID
    :param self:
    :param exception_id:
    :return:
    """
    # If ID is a string turn it into an ObjectID
    try:
        return_list = []
        if type(exception_id) is str:
            exception_id = ObjectId(exception_id)
        exception_cursor = self._db.exceptionAudits.aggregate([
            {
                '$match': {
                    'exception_id': exception_id
                }
            }, {
                '$lookup': {
                    'from': 'users',
                    'localField': 'user_id',
                    'foreignField': '_id',
                    'as': 'user'
                }
            }, {
                '$unwind': {
                    'path': '$user'
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
            }
        ])
        async for exception_audit in exception_cursor:
            return_list.append(ExceptionAuditPipeline(exception_audit, self._db))
        return return_list
    except InvalidId:
        return []
