"""Routes for resources"""
from fastapi import APIRouter, Request, HTTPException, Depends, Query
from typing import List
from dataclasses import asdict

from app.security import security_authentication
from app.models.accountOverview import ResourceCountOverview

router = APIRouter(responses={
    401: {"description": "unauthorized/Invalid authentication"},
    403: {"description": "Forbidden/Do not have access to resource/operation"}
})


@router.get('/{account_id}', response_model=ResourceCountOverview)
async def get_account_resource_count_overview(request: Request, account_id: str,
                                              security_profile=Depends(security_authentication)):
    if not (await security_profile.check_permissions(resource_account_id=account_id, level=0)):
        HTTPException(status_code=403, detail="Invalid Permissions")
    resources = await request.app.db.get_resources_by_account_id(account_id)
    compliant = 0
    non_compliant = 0
    for resource in resources:
        if await request.app.db.get_non_complaince_by_resource_id(resource.id):
            non_compliant += 1
        else:
            compliant += 1
    return {
        "compliant": compliant,
        "non_compliant": non_compliant
    }
