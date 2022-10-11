"""Routes for managing exceptions"""
from dataclasses import asdict
from fastapi import APIRouter, Request, HTTPException, Depends
from typing import List
from app.models.exceptionAudit import ExceptionAudit
from app.security import security_authentication

router = APIRouter(responses={
    401: {"description": "unauthorized/Invalid authentication"},
    403: {"description": "Forbidden/Do not have access to resource/operation"}
})


@router.get("/exemption/{exemption_id}", response_model=List[ExceptionAudit])
async def get_exception_audit_by_exemption_id(request: Request, exemption_id: str,
                                              security_profile=Depends(security_authentication)):
    """Get audit list for exemption"""
    try:
        if not (exemption := await request.app.db.get_exception_from_exception_id(exemption_id)):
            raise HTTPException(status_code=404, detail="exemption not found")
        # Check user permissions
        if not (await security_profile.check_permissions(resource_customer_id=exemption.customer.id, level=0)):
            raise HTTPException(status_code=403, detail="Invalid Permissions")
        audits = await request.app.db.get_exception_audit_by_exception_id(exemption_id)
        return_list = []
        for audit in audits:
            return_list.append({
                "id": audit.exception_audit.id,
                "action": audit.exception_audit.action,
                "old_value": audit.exception_audit.old_value,
                "new_value": audit.exception_audit.new_value,
                "old_justification": audit.exception_audit.old_justification,
                "new_justification": audit.exception_audit.new_justification,
                "old_review_date": audit.exception_audit.old_review_date,
                "new_review_date": audit.exception_audit.new_review_date,
                "old_suspended": audit.exception_audit.old_suspended,
                "new_suspended": audit.exception_audit.new_suspended,
                "user": audit.user.exception_user,
                "customer": asdict(audit.customer),
                "rule": {
                    "id": audit.rule_resource_type.rule.id,
                    "name": audit.rule_resource_type.rule.name,
                    "description": audit.rule_resource_type.rule.description,
                    "resource_type": {
                        "id": audit.rule_resource_type.resource_type.id,
                        "name": audit.rule_resource_type.resource_type.name,
                        "platform": {
                            "id": audit.rule_resource_type.platform.id,
                            "name": audit.rule_resource_type.platform.name,
                        }
                    }
                }
            })
        return return_list
    except IndexError:
        raise HTTPException(status_code=500, detail="Internal count error")
