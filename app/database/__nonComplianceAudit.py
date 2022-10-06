from __future__ import annotations
from typing import TYPE_CHECKING, List, Union, Optional

from .models import NonComplianceAudit

if TYPE_CHECKING:
    from .__init__ import DBConnector
from bson import ObjectId
from bson.errors import InvalidId


async def get_non_compliance_audit_by_id(self: 'DBConnector', non_compliance_audit_id: Union[ObjectId, str]) \
        -> Optional[NonComplianceAudit]:
    """
    Get non-compliance audit by id
    :param self:
    :param non_compliance_audit_id: non-compliance audit's ID
    :return:
    """
    try:
        if type(non_compliance_audit_id) is str:
            non_compliance_audit_id = ObjectId(non_compliance_audit_id)
        if result := await self._db.nonComplianceAudits.find_one({"_id": non_compliance_audit_id}):
            return NonComplianceAudit(result)
    except InvalidId:
        return None
