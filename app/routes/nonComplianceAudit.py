from fastapi import APIRouter, Request, HTTPException, Depends, Query
from typing import List
from dataclasses import asdict

from app.models.nonComplianceAudit import NonComplianceAudit
from app.security import security_authentication

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
    if not (await security_profile.check_permissions(
            resource_account_id=non_compliance_audit.resource.account_info.account.id, level=0)):
        raise HTTPException(status_code=403, detail="Invalid Permissions")
    return {
            "id": non_compliance_audit.non_compliance_audit.id,
            "action": non_compliance_audit.non_compliance_audit.action,
            "action_datetime": non_compliance_audit.non_compliance_audit.action_datetime,
            "user": non_compliance_audit.user.exception_user,
            "resource": {
                "id": non_compliance_audit.resource.resource.id,
                "name": non_compliance_audit.resource.resource.name,
                "reference": non_compliance_audit.resource.resource.reference,
                "last_updated": non_compliance_audit.resource.resource.last_updated,
                "account": non_compliance_audit.resource.account_info.account.api_response(
                    non_compliance_audit.resource.account_info.customer,
                    non_compliance_audit.resource.account_info.platform),
                "resource_type": non_compliance_audit.resource.resource_type_info.resource_type.api_response(
                    non_compliance_audit.resource.resource_type_info.platform),
                "metadata": non_compliance_audit.resource.resource.metadata,
            },
            "rule": {
                "id": non_compliance_audit.rule_resource_type.rule.id,
                "name": non_compliance_audit.rule_resource_type.rule.name,
                "description": non_compliance_audit.rule_resource_type.rule.description,
                "resource_type": {
                    "id": non_compliance_audit.rule_resource_type.resource_type.id,
                    "name": non_compliance_audit.rule_resource_type.resource_type.name,
                    "platform": {
                        "id": non_compliance_audit.rule_resource_type.platform.id,
                        "name": non_compliance_audit.rule_resource_type.platform.name,
                    }
                }
            }
        }


@router.get("/resource/{resource_id}", response_model=List[NonComplianceAudit])
async def get_non_compliance_audit_by_resource_id(request: Request, resource_id: str,
                                                  security_profile=Depends(security_authentication)):
    """Get Non Complaince Audit list for resource ID"""
    if not (resource := await request.app.db.get_resource_by_id(resource_id)):
        raise HTTPException(status_code=404, detail="Resource not found")
    if not (await security_profile.check_permissions(resource_account_id=resource.account_id, level=0)):
        raise HTTPException(status_code=403, detail="Invalid Permissions")
    audit = await request.app.db.get_non_compliance_audit_by_resource_id(resource_id)
    audit_list = []
    for x in audit:
        audit_list.append({
            "id": x.non_compliance_audit.id,
            "action": x.non_compliance_audit.action,
            "action_datetime": x.non_compliance_audit.action_datetime,
            "user": x.user.exception_user,
            "resource": {
                "id": x.resource.resource.id,
                "name": x.resource.resource.name,
                "reference": x.resource.resource.reference,
                "last_updated": x.resource.resource.last_updated,
                "account": x.resource.account_info.account.api_response(x.resource.account_info.customer,
                                                                        x.resource.account_info.platform),
                "resource_type": x.resource.resource_type_info.resource_type.api_response(
                    x.resource.resource_type_info.platform),
                "metadata": x.resource.resource.metadata,
            },
            "rule": {
                "id": x.rule_resource_type.rule.id,
                "name": x.rule_resource_type.rule.name,
                "description": x.rule_resource_type.rule.description,
                "resource_type": {
                    "id": x.rule_resource_type.resource_type.id,
                    "name": x.rule_resource_type.resource_type.name,
                    "platform": {
                        "id": x.rule_resource_type.platform.id,
                        "name": x.rule_resource_type.platform.name,
                    }
                }
            }
        })
    return audit_list
