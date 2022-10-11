"""Routes for user login & logout"""
from fastapi import APIRouter, Request, HTTPException, Depends
from dataclasses import asdict

from app.security import security_authentication
from app.models.user import UserProfile
from app.models.sessionInfo import UserPermissions

router = APIRouter(responses={
    401: {"description": "unauthorized/Invalid authentication"},
    403: {"description": "Forbidden/Do not have access to resource/operation"}
})


@router.get('/profile', response_model=UserProfile, responses={
    404: {"description": "No user session profile found"}
})
async def get_user_profile(security_profile=Depends(security_authentication)):
    """Get user details for the currently logged-in session."""
    return {
        "id": security_profile.session.id,
        "email": security_profile.session.email,
        "first_name": security_profile.session.first_name,
        "last_name": security_profile.session.last_name,
        "session_expiry": security_profile.session.session_expiry
    }


@router.get('/permissions', response_model=UserPermissions, responses={
    404: {"description": "No user session profile found"}
})
async def get_user_permissions(request: Request, security_profile=Depends(security_authentication)):
    """Get user role & customer permissions for the currently logged-in session."""
    response = {}
    if security_profile.session.role_id:
        if role := await request.app.db.get_role_by_id(security_profile.session.role_id):
            response["role"] = asdict(role)
    if security_profile.session.customer_id:
        if customer := await request.app.db.get_customer_by_id(security_profile.session.customer_id):
            response["customer"] = asdict(customer)
    return response

