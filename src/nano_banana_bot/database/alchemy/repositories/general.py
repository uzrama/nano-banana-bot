from sqlalchemy.ext.asyncio import AsyncSession

from nano_banana_bot.models.base import Base

from .base import BaseAlchemyRepository
from .users import UsersRepository


class Repository(BaseAlchemyRepository[Base]):
    users: UsersRepository

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session=session)
        self.users = UsersRepository(session=session)
