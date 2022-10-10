"""Handles Rules"""
from __future__ import annotations
from typing import TYPE_CHECKING, List, Union, Optional

if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId
from bson.errors import InvalidId

from app.database.models import Rule, RuleResourceTypePipeline


async def get_all_rules(self: 'DBConnector') -> List[Rule]:
    """
    Get all rules
    :param self:
    :return: List of rules
    """
    return_list = []
    async for rule in self._db.rules.find({}):
        return_list.append(Rule(rule))
    return return_list


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


async def get_rules_by_resource_type_id(self: 'DBConnector', resource_type_id: Union[ObjectId, str]) -> List[Rule]:
    """
    Get list of rules from a resource_type id
    :param self:
    :param resource_type_id: resource_type id
    :return: List of rules that apply to resources
    """
    return_list = []
    try:
        # If ID is a string turn it into an ObjectID
        if type(resource_type_id) is str:
            resource_type_id = ObjectId(resource_type_id)
        async for rule in self._db.rules.find({"resource_type_id": resource_type_id}):
            return_list.append(Rule(rule))
        return return_list
    except InvalidId:
        return []


async def rules_by_resource_type_pipeline(self: 'DBConnector', resource_type_id: Union[ObjectId, str]) -> \
        List[RuleResourceTypePipeline]:
    return_list = []
    try:
        # If ID is a string turn it into an ObjectID
        if type(resource_type_id) is str:
            resource_type_id = ObjectId(resource_type_id)
        rule_cursor = self._db.rules.aggregate([
            {
                '$match': {
                    'type_id': resource_type_id
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
        async for rule_aggregation in rule_cursor:
            return_list.append(RuleResourceTypePipeline(rule_aggregation))
        return return_list
    except InvalidId:
        return []


async def get_all_rules_pipeline(self: 'DBConnector') -> List[RuleResourceTypePipeline]:
    return_list = []
    rule_cursor = self._db.rules.aggregate([
            {
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
    async for rule_aggregation in rule_cursor:
        return_list.append(RuleResourceTypePipeline(rule_aggregation))
    return return_list
