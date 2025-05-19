from fastapi import Depends, APIRouter, Response
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.auth import create_access_token, create_refresh_token
from app.services.auth import (
    validate_user,
    validate_refresh_token,
    get_access_refresh_tokens_jti,
    blacklist_access_refresh_token,
)
from app.schemas.auth import AccessTokenSchema
from app.db.models.users import UserORM
from app.db.database import get_db


router = APIRouter(prefix="/auth")


@router.post("/login", response_model=AccessTokenSchema)
async def issue_refresh_access_tokens(
    response: Response, user_obj: UserORM = Depends(validate_user)
):
    """Not using 'secure=True' flag when setting refresh token cookie, because dev server"""
    access_token = create_access_token(username=user_obj.username)
    refresh_token = create_refresh_token(username=user_obj.username)
    response.set_cookie(key="refresh", value=refresh_token, httponly=True, samesite="lax")
    return AccessTokenSchema(access_token=access_token)


@router.post("/refresh", response_model=AccessTokenSchema)
async def refresh_access_token(user_obj: UserORM = Depends(validate_refresh_token)):
    access_token = create_access_token(username=user_obj.username)
    return AccessTokenSchema(access_token=access_token)


@router.post("/logout")
async def logout_user(
    jti_tuple: tuple = Depends(get_access_refresh_tokens_jti), db: AsyncSession = Depends(get_db)
):
    await blacklist_access_refresh_token(db=db, jti_tuple=jti_tuple)
    return {"status": "success"}
