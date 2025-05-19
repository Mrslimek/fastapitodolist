from pydantic import BaseModel
from app.utils.schemas import NonEmptyString, PwdStr


class UserBase(BaseModel):
    username: NonEmptyString
    password: PwdStr
    first_name: NonEmptyString
    last_name: NonEmptyString | None = None
    
