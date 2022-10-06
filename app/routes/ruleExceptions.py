"""Routes for user rules"""
from fastapi import APIRouter, Request, HTTPException, Depends, Query
from typing import List, Optional, Union
from dataclasses import asdict
from datetime import datetime
from datetime import timedelta

from app.security import security_authentication
from app.models.exceptions import RuleException, AccountRuleException

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


@router.get('/account/{account_id}/overdue', response_model=List[AccountRuleException])
async def get_account_overdue_exceptions(request: Request, account_id: str,
                                         security_profile=Depends(security_authentication)):
    """Get exceptions overdue for review"""
    # Check if user has permission
    if not (await security_profile.check_permissions(resource_account_id=account_id, level=0)):
        HTTPException(status_code=403, detail="Invalid Permissions")
    now = datetime.utcnow()
    rule_exceptions = await request.app.db.get_exception_by_date_account_id(account_id, None, now)
    return_list = []
    for rule_exception in rule_exceptions:
        resource_type = {
            "id": rule_exception.rule_resource_type.resource_type.id,
            "name": rule_exception.rule_resource_type.resource_type.name,
            "platform": {
                "id": rule_exception.rule_resource_type.platform.id,
                "name": rule_exception.rule_resource_type.platform.name,
            }
        }
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
                "resource_type": resource_type
            },
            "resource": {
                "id": rule_exception.resource.id,
                "name": rule_exception.resource.name,
                "reference": rule_exception.resource.reference,
                "resource_type": resource_type,
                "last_updated": rule_exception.resource.last_updated,
                "metadata": rule_exception.resource.metadata
            }
        })
    return return_list


@router.get('/account/{account_id}/upcoming', response_model=List[AccountRuleException])
async def get_account_upcoming_exceptions(request: Request, account_id: str,
                                          days: Union[int, None] = 7,
                                          security_profile=Depends(security_authentication)):
    """Get exceptions upcoming for review"""
    # Check if user has permission
    if not (await security_profile.check_permissions(resource_account_id=account_id, level=0)):
        HTTPException(status_code=403, detail="Invalid Permissions")
    now = datetime.utcnow() + timedelta(days=days)
    end = datetime.utcnow()
    rule_exceptions = await request.app.db.get_exception_by_date_account_id(account_id, end, now)
    return_list = []
    for rule_exception in rule_exceptions:
        resource_type = {
            "id": rule_exception.rule_resource_type.resource_type.id,
            "name": rule_exception.rule_resource_type.resource_type.name,
            "platform": {
                "id": rule_exception.rule_resource_type.platform.id,
                "name": rule_exception.rule_resource_type.platform.name,
            }
        }
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
                "resource_type": resource_type
            },
            "resource": {
                "id": rule_exception.resource.id,
                "name": rule_exception.resource.name,
                "reference": rule_exception.resource.reference,
                "resource_type": resource_type,
                "last_updated": rule_exception.resource.last_updated,
                "metadata": rule_exception.resource.metadata
            }
        })
    return return_list
