"""FastAPI Security Dependencies"""
from fastapi import Request, HTTPException, Depends
from typing import Optional

from .models import SessionSecurityProfile


async def get_user_session(request: Request) -> Optional[SessionSecurityProfile]:
    """Gets the user's security profile from their cookie session"""
    return await request.app.security.get_security_profile(request)


async def security_authentication(user_session=Depends(get_user_session)) -> SessionSecurityProfile:
    """
    Gets the user's security profile. Will raise an exception if no profile is found
    :return: Security Profile
    """
    if not user_session:
        raise HTTPException(status_code=401, detail="Not Authorised / Invalid API Key")
    elif user_session:
        return user_session
