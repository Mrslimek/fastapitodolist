from sqlalchemy import String, Text, Enum, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.utils.enums import TaskStatus, get_enum_values
from app.db.database import Base
from app.db.models.users import UserORM


class TaskORM(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, name="Title")
    description: Mapped[str] = mapped_column(Text, name="Description", nullable=True)
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, values_callable=get_enum_values, name="task_status"),
        default=TaskStatus.NEW,
    )
    user_id: Mapped[UserORM] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    user = relationship(UserORM, back_populates="tasks")
