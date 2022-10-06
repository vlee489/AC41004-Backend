from fastapi import APIRouter, Request, HTTPException, Depends, Query
from typing import List
from dataclasses import asdict

from app.models.nonComplianceAudit import NonComplianceAudit
from app.security import security_authentication
from app.models.resources import Resource

router = APIRouter(responses={
    401: {"description": "unauthorized/Invalid authentication"},
    403: {"description": "Forbidden/Do not have access to resource/operation"}
})


@router.get("/{non_compliance_audit_id}", response_model=NonComplianceAudit)
async def get_non_compliance_audit_by_id(
        request: Request,
        non_compliance_audit_id: str,
        security_profile=Depends(security_authentication)
    ):
    """Get a single non-compliance audit by its id"""
    if not (non_compliance_audit := await request.app.db.get_non_compliance_audit_by_id(non_compliance_audit_id)):
        raise HTTPException(status_code=404, detail="Resource not found")
    if not (resource := await request.app.db.get_resource_by_id(non_compliance_audit.resource_id)):
        raise HTTPException(status_code=404, detail="Resource not found")
    if not (await security_profile.check_permissions(resource_account_id=resource.account_id, level=0)):
        raise HTTPException(status_code=403, detail="Invalid Permissions")
    return asdict(non_compliance_audit)
