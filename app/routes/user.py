"""Routes for user login & logout"""
from fastapi import APIRouter, Request, HTTPException, Depends, Query

from app.security import security_authentication
from app.models.user import UserProfile

router = APIRouter(responses={
    401: {"description": "unauthorized/Invalid authentication"},
    403: {"description": "Forbidden/Do not have access to resource/operation"}
})


@router.get('/profile', response_model=UserProfile, responses={
    404: {"description": "No user session profile found"}
})
async def get_user_profile(security_profile=Depends(security_authentication)):
    """Get user details for the currently logged-in session.<br/><i>Doesn't work for API key access!</i>"""
    return {
        "id": security_profile.session.id,
        "email": security_profile.session.email,
        "first_name": security_profile.session.first_name,
        "last_name": security_profile.session.last_name,
        "session_expiry": security_profile.session.session_expiry
    }
