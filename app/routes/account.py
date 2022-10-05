"""Routes for user login & logout"""
from fastapi import APIRouter, Request, HTTPException, Depends, Query
from typing import List
from dataclasses import asdict

from app.security import security_authentication
from app.models.account import Account

router = APIRouter(responses={
    401: {"description": "unauthorized/Invalid authentication"},
    403: {"description": "Forbidden/Do not have access to resource/operation"}
})


@router.get('/access', response_model=List[Account], responses={
    404: {"description": "No user session profile found"}
})
async def get_user_accounts(request: Request, security_profile=Depends(security_authentication)):
    """Get Accounts the user has access to."""
    if security_profile.session.customer_id:
        return_list = []
        # Store customer and platform in memory when building response
        customers = {}
        platforms = {}
        if accounts := await request.app.db.get_account_by_customer_id(security_profile.session.customer_id):
            for account in accounts:
                platform_instance, customer_instance = None, None
                # Get Platform
                if account.platform_id in platforms:
                    platform_instance = platforms[account.platform_id]
                else:
                    if platform := await request.app.db.get_platform_by_id(account.platform_object_id):
                        platform_instance = asdict(platform)
                        platforms[platform.id] = platform_instance
                # Get Customer
                if account.customer_id in customers:
                    customer_instance = customers[account.customer_id]
                else:
                    if customer := await request.app.db.get_customer_by_id(account.customer_id):
                        customer_instance = asdict(customer)
                        platforms[customer.id] = customers
                # create instance of account
                return_list.append({
                    "id": account.id,
                    "name": account.name,
                    "reference": account.reference,
                    "customer": customer_instance,
                    "platform": platform_instance
                })
        return return_list  # return list of accounts


@router.get("/{account_id}", response_model=Account)
async def get_account_by_id(request: Request, account_id: str, security_profile=Depends(security_authentication)):
    """Get a single user account by customer id"""
    if not (await security_profile.check_permissions(resource_account_id=account_id, level=0.0)):
        raise HTTPException(status_code=403, detail="Invalid Permissions")
    if not (account := await request.app.db.get_account_by_id(account_id)):
        raise HTTPException(status_code=404, detail="Resource not found")
    platform = await request.app.db.get_platform_by_id(account.platform_id)
    customer = await request.app.db.get_customer_by_id(account.customer_id)
    return {
        "id": account_id,
        "name": account.name,
        "reference": account.reference,
        "customer": customer,
        "platform": platform,
    }

