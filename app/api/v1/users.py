from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.users import create_user, save_user_in_db, is_username_available
from app.schemas.users import UserBase
from app.db.database import get_db
from app.utils.exceptions import UsernameIsTakenError


router = APIRouter(prefix="/users")


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_and_save_user(user_data: UserBase, db: AsyncSession = Depends(get_db)):
    if await is_username_available(db=db, username=user_data.username):
        user_obj = create_user(**user_data.model_dump())
        await save_user_in_db(db=db, user_obj=user_obj)
        return {"status": "success"}
    else:
        raise UsernameIsTakenError(username=user_data.username)
