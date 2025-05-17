from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.users import UserBase, UserLogin
from app.schemas.auth import AccessTokenSchema
from app.db.database import get_db
from app.services.auth import (
    create_user,
    save_user_in_db,
    validate_user,
)
from app.utils.auth import encode_jwt
from app.config import settings


router = APIRouter(prefix="/auth")


@router.post("/register")
async def register_user(user_data: UserBase, db: AsyncSession = Depends(get_db)):
    user_obj = create_user(**user_data.model_dump())
    await save_user_in_db(db=db, user_obj=user_obj)
    return {"status": "success"}


@router.post("/login", response_model=AccessTokenSchema)
async def login_user(user_obj: UserLogin = Depends(validate_user)):
    jwt_payload = {"sub": user_obj.username}
    access_token = encode_jwt(
        payload=jwt_payload, expire_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return AccessTokenSchema(access_token=access_token, token_type="Bearer")
