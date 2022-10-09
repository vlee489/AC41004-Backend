"""Routes for user rules"""
from dataclasses import asdict
from datetime import datetime
from datetime import timedelta
from typing import List, Union

from fastapi import APIRouter, Request, HTTPException, Depends, BackgroundTasks

from app.database.models import Account
from app.database.models.input import NewExceptionAudit, UpdateExceptionAudit
from app.models import AddExceptionResponse, AddExceptionRequest
from app.models.exception import EditExceptionRequest
from app.models.exceptions import RuleException, AccountRuleException
from app.models.response.exception import EditExceptionResponse
from app.security import security_authentication

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


@router.post("/", response_model=AddExceptionResponse)
async def add_exception(request: Request, exception: AddExceptionRequest, background_tasks: BackgroundTasks,
                        security_profile=Depends(security_authentication)):
    # Getting all the required details
    if not (resource := await request.app.db.get_resource_by_id(exception.resource_id)):
        raise HTTPException(status_code=404, detail="Resource not found")
    if not (await security_profile.check_permissions(resource_account_id=resource.account_id, level=1)):
        raise HTTPException(status_code=403, detail="Invalid Permissions")
    if not (account := await request.app.db.get_account_by_id(resource.account_id)):
        raise HTTPException(status_code=500)

    # Checking that the IDs exist, if they haven't been checked already
    if not (rule := await request.app.db.get_rule_by_id(exception.rule_id)):
        raise HTTPException(status_code=404, detail="Rule not found")
    if rule.resource_type_id != resource.resource_type_id:
        raise HTTPException(status_code=400, detail="Resource and Rule types do not match!")

    inserted_id = await request.app.db.add_exception(
        customer_id=account.customer_object_id,
        rule_id=exception.rule_id,
        last_updated_by=security_profile.session.id,
        exception_value=resource.reference,  # exception value is linked to the resources reference field
        justification=exception.justification,
        review_date=exception.review_date,
        last_updated=datetime.now()
    )
    # Add new exception to Audit log as background task
    if not (exception_entry := await request.app.db.get_exception_from_exception_id(inserted_id)):
        raise HTTPException(status_code=500, detail="Unable to add exception")
    audit = NewExceptionAudit(rule_exception=exception_entry.exception, user_id=security_profile.session.id,
                              new_value=resource.reference, new_justification=exception.justification,
                              new_review_date=exception.review_date)
    background_tasks.add_task(request.app.db.add_exception_audit, new_audit=audit)
    return {"inserted_id": str(inserted_id)}


@router.patch("/{exception_id}", response_model=EditExceptionResponse)
async def update_exception(request: Request, exception: EditExceptionRequest, exception_id: str,
                           background_tasks: BackgroundTasks, security_profile=Depends(security_authentication)):
    # Get and check if exception exists
    if not (exception_instance := await request.app.db.get_exception_from_exception_id(exception_id)):
        raise HTTPException(status_code=404, detail="Exception not found")
    # Check user permissions
    if not (await security_profile.check_permissions(resource_customer_id=exception_instance.customer.id, level=1)):
        raise HTTPException(status_code=403, detail="Invalid Permissions")
    # Update Exception
    acknowledged = await request.app.db.update_exception(
        exception_id=exception_id,

        last_updated_by=security_profile.session.id,
        last_updated=datetime.utcnow(),

        exception_value=exception.exception_value,
        justification=exception.justification,
        review_date=exception.review_date
    )
    if acknowledged:
        audit = UpdateExceptionAudit(rule_exception=exception_instance.exception, user_id=security_profile.session.id,
                                     new_value=exception.exception_value, new_justification=exception.justification,
                                     new_review_date=exception.review_date)
        background_tasks.add_task(request.app.db.update_exception_audit, updated_audit=audit)
        return {"status": True}
    else:
        raise HTTPException(status_code=500, detail="DB acknowledgment error")


# async def __get_account_and_check_ids(
#         request: Request,
#         security_profile: Depends,
#         resource_id: str,
#         rule_id: str,
# ) -> Account:
#     # Getting all the required details
#     if not (resource := await request.app.db.get_resource_by_id(resource_id)):
#         raise HTTPException(status_code=404, detail="Resource not found")
#     if not (await security_profile.check_permissions(resource_account_id=resource.account_id, level=1)):
#         raise HTTPException(status_code=403, detail="Invalid Permissions")
#     if not (account := await request.app.db.get_account_by_id(resource.account_id)):
#         raise HTTPException(status_code=500)
#
#     # Checking that the IDs exist, if they haven't been checked already
#     if not await request.app.db.get_rule_by_id(rule_id):
#         raise HTTPException(status_code=404, detail="Rule not found")
#
#     return account
