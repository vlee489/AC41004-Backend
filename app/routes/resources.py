"""Routes for resources"""
from fastapi import APIRouter, Request, HTTPException, Depends
from typing import List

from app.security import security_authentication
from app.models.resources import Resource

router = APIRouter(responses={
    401: {"description": "unauthorized/Invalid authentication"},
    403: {"description": "Forbidden/Do not have access to resource/operation"}
})


@router.get('/{resource_id}', response_model=Resource)
async def get_resource(request: Request, resource_id: str, security_profile=Depends(security_authentication)):
    """Get details of a resource"""
    if resource := await request.app.db.get_resource_by_id(resource_id):
        # Check if user has permission
        if not (await security_profile.check_permissions(resource_account_id=resource.account_id, level=0)):
            raise HTTPException(status_code=403, detail="Invalid Permissions")
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
            "id": resource.id,
            "name": resource.name,
            "reference": resource.reference,
            "last_updated": resource.last_updated,
            "account": account.api_response(account_customer, account_platform),
            "resource_type": resource_type.api_response(resource_type_platform),
            "metadata": resource.metadata
        }
    else:
        raise HTTPException(status_code=404, detail="Resource not found")


@router.get('/account/{account_id}', response_model=List[Resource])
async def get_account_resources(request: Request, account_id: str, security_profile=Depends(security_authentication)):
    if not (await security_profile.check_permissions(resource_account_id=account_id, level=0)):
        raise HTTPException(status_code=403, detail="Invalid Permissions")
    resources = await request.app.db.get_resources_by_account_id(account_id)
    return_list = []
    for resource in resources:
        return_list.append({
            "id": resource.resource.id,
            "name": resource.resource.name,
            "reference": resource.resource.reference,
            "last_updated": resource.resource.last_updated,
            "account": resource.account_info.account.api_response(resource.account_info.customer,
                                                                  resource.account_info.platform),
            "resource_type": resource.resource_type_info.resource_type.api_response(
                resource.resource_type_info.platform),
            "metadata": resource.resource.metadata
        })
    return return_list
