"""Routes for managing exceptions"""
from datetime import datetime
from fastapi import APIRouter, Request, HTTPException, Depends, Query
from app.models import AddExceptionResponse, AddExceptionRequest
from app.security import security_authentication

router = APIRouter(responses={
    401: {"description": "unauthorized/Invalid authentication"},
    403: {"description": "Forbidden/Do not have access to resource/operation"}
})


@router.post("/add", response_model=AddExceptionResponse)
async def add_exception(
        request: Request,
        exception: AddExceptionRequest,
        security_profile=Depends(security_authentication)
):
    # Getting all the required details
    if not (resource := await request.app.db.get_resource_by_id(exception.resource_id)):
        raise HTTPException(status_code=404, detail="Resource not found")
    if not (await security_profile.check_permissions(resource_account_id=resource.account_id, level=1)):
        raise HTTPException(status_code=403, detail="Invalid Permissions")
    if not (account := await request.app.db.get_account_by_id(resource.account_id)):
        raise HTTPException(status_code=500)  # A resource should always have an existing account

    # Checking that the IDs exist, if they haven't been checked already
    if not await request.app.db.get_rule_by_id(exception.rule_id):
        raise HTTPException(status_code=404, detail="Rule not found")

    inserted_id = await request.app.db.add_exception(
        customer_id=account.customer_id,
        rule_id=exception.rule_id,
        last_updated_by=security_profile.session.id,
        exception_value=exception.resource_id,
        justification=exception.justification,
        review_date=exception.review_date,
        last_updated=datetime.now()
    )
    return {"inserted_id": str(inserted_id)}
