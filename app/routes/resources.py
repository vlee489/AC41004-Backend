"""Routes for resources"""
from fastapi import APIRouter, Request, HTTPException, Depends, Query
from typing import List
from dataclasses import asdict

from app.security import security_authentication
from app.models.resources import Resource

router = APIRouter(responses={
    401: {"description": "unauthorized/Invalid authentication"},
    403: {"description": "Forbidden/Do not have access to resource/operation"}
})


@router.get('/{resource_id}', response_model=Resource)
async def get_resource(request: Request, resource_id: str, security_profile=Depends(security_authentication)):
    """Get details of a resource"""
    # TODO CHECK USER HAS ACCESS TO ACCOUNT
    if resource := await request.app.db.get_resource_by_id(resource_id):
        account = await request.app.db.get_account_by_id(resource.account_id)
        resource_type = await request.app.db.get_resource_type_by_id(resource.resource_type_id)
        if (not account) and (not resource_type):
            raise HTTPException(status_code=500, detail="Internal Graph Error")
        account_platform = await request.app.db.get_platform_by_id(account.platform_id)
        account_customer = await request.app.db.get_customer_by_id(account.customer_id)
        if resource_type.platform_id == account_platform.id:
            resource_type_platform = account_platform
        else:
            resource_type_platform = await request.app.db.get_platform_by_id(resource_type.platform_id)
        return {
            "reference": resource.reference,
            "last_updated": resource.last_updated,
            "account": account.api_response(account_customer, account_platform),
            "resource_type": resource_type.api_response(resource_type_platform),
            "metadata": resource.metadata
        }
    else:
        raise HTTPException(status_code=404, detail="Resource not found")


