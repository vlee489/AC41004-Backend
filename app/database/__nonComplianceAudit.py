from __future__ import annotations
from typing import TYPE_CHECKING, List, Union, Optional

from .models import NonComplianceAudit, NonCompliantAuditPipeline

if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId
from bson.errors import InvalidId


async def get_non_compliance_audit_by_id(self: 'DBConnector', non_compliance_audit_id: Union[ObjectId, str]) \
        -> Optional[NonCompliantAuditPipeline]:
    """
    Get non-compliance audit by id
    :param self:
    :param non_compliance_audit_id: non-compliance audit's ID
    :return:
    """
    try:
        if type(non_compliance_audit_id) is str:
            non_compliance_audit_id = ObjectId(non_compliance_audit_id)

        audit_cursor = self._db.nonComplianceAudits.aggregate([
            {
                '$match': {
                    '_id': non_compliance_audit_id
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
                    'from': 'resources',
                    'localField': 'resource_id',
                    'foreignField': '_id',
                    'as': 'resource'
                }
            }, {
                '$unwind': {
                    'path': '$resource'
                }
            }, {
                '$lookup': {
                    'from': 'accounts',
                    'localField': 'resource.account_id',
                    'foreignField': '_id',
                    'as': 'resource.account'
                }
            }, {
                '$unwind': {
                    'path': '$resource.account'
                }
            }, {
                '$lookup': {
                    'from': 'platforms',
                    'localField': 'resource.account.platform_id',
                    'foreignField': '_id',
                    'as': 'resource.account.platform'
                }
            }, {
                '$unwind': {
                    'path': '$resource.account.platform'
                }
            }, {
                '$lookup': {
                    'from': 'customers',
                    'localField': 'resource.account.customer_id',
                    'foreignField': '_id',
                    'as': 'resource.account.customer'
                }
            }, {
                '$unwind': {
                    'path': '$resource.account.customer'
                }
            }, {
                '$lookup': {
                    'from': 'resourceTypes',
                    'localField': 'resource.type_id',
                    'foreignField': '_id',
                    'as': 'resource.resource_type'
                }
            }, {
                '$unwind': {
                    'path': '$resource.resource_type'
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
                    'from': 'platforms',
                    'localField': 'resource.resource_type.platform_id',
                    'foreignField': '_id',
                    'as': 'resource.resource_type.platform'
                }
            }, {
                '$unwind': {
                    'path': '$resource.resource_type.platform'
                }
            }
        ])
        return_list = []
        async for audit in audit_cursor:
            return_list.append(NonCompliantAuditPipeline(audit, self._db))
        if len(return_list) > 1:
            raise IndexError("Too many objects")
        elif len(return_list) == 0:
            return None
        else:
            return return_list[0]
    except InvalidId:
        return None


async def get_non_compliance_audit_by_resource_id(self: 'DBConnector', resource_id: Union[ObjectId, str]) -> \
        List[NonCompliantAuditPipeline]:
    try:
        if type(resource_id) is str:
            resource_id = ObjectId(resource_id)
        audit_cursor = self._db.nonComplianceAudits.aggregate([
            {
                '$match': {
                    'resource_id': resource_id
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
                    'from': 'resources',
                    'localField': 'resource_id',
                    'foreignField': '_id',
                    'as': 'resource'
                }
            }, {
                '$unwind': {
                    'path': '$resource'
                }
            }, {
                '$lookup': {
                    'from': 'accounts',
                    'localField': 'resource.account_id',
                    'foreignField': '_id',
                    'as': 'resource.account'
                }
            }, {
                '$unwind': {
                    'path': '$resource.account'
                }
            }, {
                '$lookup': {
                    'from': 'platforms',
                    'localField': 'resource.account.platform_id',
                    'foreignField': '_id',
                    'as': 'resource.account.platform'
                }
            }, {
                '$unwind': {
                    'path': '$resource.account.platform'
                }
            }, {
                '$lookup': {
                    'from': 'customers',
                    'localField': 'resource.account.customer_id',
                    'foreignField': '_id',
                    'as': 'resource.account.customer'
                }
            }, {
                '$unwind': {
                    'path': '$resource.account.customer'
                }
            }, {
                '$lookup': {
                    'from': 'resourceTypes',
                    'localField': 'resource.type_id',
                    'foreignField': '_id',
                    'as': 'resource.resource_type'
                }
            }, {
                '$unwind': {
                    'path': '$resource.resource_type'
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
                    'from': 'platforms',
                    'localField': 'resource.resource_type.platform_id',
                    'foreignField': '_id',
                    'as': 'resource.resource_type.platform'
                }
            }, {
                '$unwind': {
                    'path': '$resource.resource_type.platform'
                }
            }
        ])
        return_list = []
        async for audit in audit_cursor:
            return_list.append(NonCompliantAuditPipeline(audit, self._db))
        return return_list
    except InvalidId:
        return []
