from app.db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text, Integer
from app.utils.auth import hash_password


class UserORM(Base):
    """
    SQLAlchemy.orm User model
    _password stores pbkdf2_sha256 encrypted password
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, name="First name")
    last_name: Mapped[str] = mapped_column(Text, name="Last name", nullable=True)
    username: Mapped[str] = mapped_column(String, name="Username", unique=True)
    _password: Mapped[str] = mapped_column(String, name="Password")

    tasks = relationship("TaskORM", back_populates="user")

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str):
        self._password = hash_password(password)

    @staticmethod
    def create(username: str, password: str, first_name: str, last_name: str | None) -> "UserORM":
        user_obj = UserORM(username=username, first_name=first_name, last_name=last_name)
        user_obj.password = password
        return user_obj
