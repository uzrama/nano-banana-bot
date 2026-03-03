from typing import Any, cast

from sqlalchemy import select
from sqlalchemy.sql.functions import count

from nano_banana_bot.models.user import User

from .base import BaseAlchemyRepository


class UsersRepository(BaseAlchemyRepository[User]):
    async def get(self, user_id: int) -> User | None:
        return await self._get(User, User.id == user_id)

    async def update(self, user_id: int, **data: Any) -> User | None:
        return await self._update(User, User.id == user_id, load_result=True, **data)

    async def count(self) -> int:
        return cast(int, await self.session.scalar(select(count(User.id))))
