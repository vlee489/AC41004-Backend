"""Routes for user login & logout"""
from fastapi import APIRouter, Request, HTTPException, Depends, Query

from app.models import LoginResponse, LoginCredentials

router = APIRouter()


@router.post("/login", response_model=LoginResponse)
async def login(request: Request, credentials: LoginCredentials):
    """User Login"""
    if success := await request.app.security.create_session(request, credentials.email, credentials.password):
        return {"status": success}
    else:
        raise HTTPException(status_code=401, detail="Invalid Username/Password")


@router.get("/logout", response_model=LoginResponse)
async def logout(request: Request):
    """User Logout"""
    if success := await request.app.security.delete_session(request):
        return {"status": success}
    else:
        raise HTTPException(status_code=401, detail="No valid session found")

