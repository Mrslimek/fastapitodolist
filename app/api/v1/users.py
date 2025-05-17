from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.users import create_user, save_user_in_db
from app.schemas.users import UserBase
from app.db.database import get_db


router = APIRouter(prefix="/users")


@router.post("/register")
async def create_and_save_user(user_data: UserBase, db: AsyncSession = Depends(get_db)):
    user_obj = create_user(**user_data.model_dump())
    await save_user_in_db(db=db, user_obj=user_obj)
    return {"status": "success"}
