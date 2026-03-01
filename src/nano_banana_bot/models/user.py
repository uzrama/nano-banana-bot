from datetime import datetime

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from nano_banana_bot.schemas import UserScheme
from nano_banana_bot.utils.custom_types import Int64

from .base import Base
from .mixins import TimestampMixin


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[Int64] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    language: Mapped[str] = mapped_column(String(length=2))
    language_code: Mapped[str | None] = mapped_column()
    blocked_at: Mapped[datetime | None] = mapped_column()

    def scheme(self) -> UserScheme:
        return UserScheme.model_validate(self)
