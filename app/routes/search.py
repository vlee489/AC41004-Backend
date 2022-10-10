"""Routes for searching"""
from fastapi import APIRouter, Request, HTTPException, Depends, Query
from typing import List
from dataclasses import asdict

from app.security import security_authentication
from app.models.resources import SearchResource

router = APIRouter(responses={
    401: {"description": "unauthorized/Invalid authentication"},
    403: {"description": "Forbidden/Do not have access to resource/operation"}
})


@router.get('/account/{account_id}/{query}', response_model=List[SearchResource])
async def get_resource(request: Request, account_id: str, query: str,
                       security_profile=Depends(security_authentication)):
    if not (await security_profile.check_permissions(resource_account_id=account_id, level=0)):
        raise HTTPException(status_code=403, detail="Invalid Permissions")
    search = await request.app.db.search_account_id_resources(query, account_id)
    return [asdict(r) for r in search]  # Return search results


