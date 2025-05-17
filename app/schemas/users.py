from pydantic import BaseModel


class UserBase(BaseModel):
    username: str
    # TODO: Не меньше 6 символов
    password: str
    first_name: str
    last_name: str | None = None
    

class UserLogin(BaseModel):
    username: str
    password: str
