"""Handles Resources"""
from __future__ import annotations
from typing import TYPE_CHECKING, List, Union, Optional

if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId
from bson.errors import InvalidId

from app.database.models import Resource, NonComplaintResourceCount, ResourcePipeline


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
        if document := await self._db.resources.find_one({"_id": resource_id}):
            return Resource(document)
    except InvalidId:
        return None


async def get_resources_by_account_id(self: 'DBConnector', account_id: Union[ObjectId, str]) -> List[ResourcePipeline]:
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
        resource_cursor = self._db.resources.aggregate([
            {
                '$match': {
                    'account_id': account_id
                }
            }, {
                '$lookup': {
                    'from': 'resourceTypes',
                    'localField': 'type_id',
                    'foreignField': '_id',
                    'as': 'resource_type'
                }
            }, {
                '$unwind': {
                    'path': '$resource_type'
                }
            }, {
                '$lookup': {
                    'from': 'accounts',
                    'localField': 'account_id',
                    'foreignField': '_id',
                    'as': 'account'
                }
            }, {
                '$unwind': {
                    'path': '$account'
                }
            }, {
                '$lookup': {
                    'from': 'platforms',
                    'localField': 'account.platform_id',
                    'foreignField': '_id',
                    'as': 'account.platform'
                }
            }, {
                '$unwind': {
                    'path': '$account.platform'
                }
            }, {
                '$lookup': {
                    'from': 'customers',
                    'localField': 'account.customer_id',
                    'foreignField': '_id',
                    'as': 'account.customer'
                }
            }, {
                '$unwind': {
                    'path': '$account.customer'
                }
            }, {
                '$lookup': {
                    'from': 'platforms',
                    'localField': 'resource_type.platform_id',
                    'foreignField': '_id',
                    'as': 'resource_type.platform'
                }
            }, {
                '$unwind': {
                    'path': '$resource_type.platform'
                }
            }
        ])
        async for r in resource_cursor:
            resources.append(ResourcePipeline(r))
        return resources
    except InvalidId:
        return []


async def get_non_compliant_resources_by_account_id(self: 'DBConnector', account_id: Union[ObjectId, str]) -> \
        List[Resource]:
    """
    Get non compliant Resources with the Account ID
    :param self:
    :param account_id: Account's ID
    :return: list of resources for account that aren't compliant
    """
    resources = []
    try:
        # If ID is a string turn it into an ObjectID
        if type(account_id) is str:
            account_id = ObjectId(account_id)
        resource_cursor = self._db.resources.aggregate([
            {
                '$match': {
                    'account_id': account_id
                }
            }, {
                '$lookup': {
                    'from': 'nonCompliances',
                    'localField': '_id',
                    'foreignField': 'resource_id',
                    'as': 'non_compliance'
                }
            }, {
                '$match': {
                    'non_compliance': {
                        '$exists': True,
                        '$not': {
                            '$size': 0
                        }
                    }
                }
            }, {
                '$unwind': {
                    'path': '$non_compliance'
                }
            }
        ])
        async for r in resource_cursor:
            resources.append(Resource(r))
        return resources
    except InvalidId:
        return []


async def get_overview_count_by_account_id(self: 'DBConnector', account_id: Union[ObjectId, str]) -> \
        Optional[NonComplaintResourceCount]:
    try:
        # If ID is a string turn it into an ObjectID
        if type(account_id) is str:
            account_id = ObjectId(account_id)
        compliant = 0
        non_compliant = 0
        resource_cursor = self._db.resources.aggregate([
            {
                '$match': {
                    'account_id': ObjectId('633ad7aca938b45d958ae772')
                }
            }, {
                '$lookup': {
                    'from': 'nonCompliances',
                    'localField': '_id',
                    'foreignField': 'resource_id',
                    'as': 'non_complainces'
                }
            }, {
                '$project': {
                    'non_complaint_rules': {
                        '$size': '$non_complainces'
                    }
                }
            }
        ])
        async for r in resource_cursor:
            if r['non_complaint_rules'] > 0:
                non_compliant += 1
            else:
                compliant += 1
        return NonComplaintResourceCount(compliant, non_compliant)
    except InvalidId:
        return None
