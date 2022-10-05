"""Routes for user rules"""
from fastapi import APIRouter, Request, HTTPException, Depends, Query
from typing import List
from dataclasses import asdict

from app.security import security_authentication
from app.models.exceptions import RuleException

router = APIRouter(responses={
    401: {"description": "unauthorized/Invalid authentication"},
    403: {"description": "Forbidden/Do not have access to resource/operation"}
})


@router.get('/resource/{resource_id}', response_model=List[RuleException])
async def get_resource_exceptions(request: Request, resource_id: str,
                                  security_profile=Depends(security_authentication)):
    """Get exceptions for a resource"""
    if resource := await request.app.db.get_resource_by_id(resource_id):
        # Check if user has permission
        if not (await security_profile.check_permissions(resource_account_id=resource.account_id, level=0)):
            HTTPException(status_code=403, detail="Invalid Permissions")
        rule_exceptions = await request.app.db.get_exception_from_exception_value(resource.reference)
        return_list = []
        for rule_exception in rule_exceptions:
            return_list.append({
                "id": rule_exception.exception.id,
                "exception_value": rule_exception.exception.exception_value,
                "justification": rule_exception.exception.justification,
                "review_date": rule_exception.exception.review_date,
                "last_updated": rule_exception.exception.last_updated,
                "last_updated_by": rule_exception.user.exception_user,
                "customer": asdict(rule_exception.customer),
                "rule": {
                    "id": rule_exception.rule_resource_type.rule.id,
                    "name": rule_exception.rule_resource_type.rule.name,
                    "description": rule_exception.rule_resource_type.rule.description,
                    "resource_type": {
                        "id": rule_exception.rule_resource_type.resource_type.id,
                        "name": rule_exception.rule_resource_type.resource_type.name,
                        "platform": {
                            "id": rule_exception.rule_resource_type.platform.id,
                            "name": rule_exception.rule_resource_type.platform.name,
                        }
                    }
                }
            })
        return return_list
    else:
        raise HTTPException(status_code=404, detail="Resource not found")
