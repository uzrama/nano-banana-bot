from typing import override
from sqlalchemy.ext.asyncio import AsyncSession

from nano_banana_bot.database.base import BaseUnitOfWork
from nano_banana_bot.models.base import Base


class UoW(BaseUnitOfWork[Base]):
    session: AsyncSession

    __slots__ = ("session",)

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @override
    async def commit(self, *instances: Base) -> None:
        if instances:
            self.session.add_all(instances)
        await self.session.commit()

    @override
    async def merge(self, *instances: Base) -> None:
        for instance in instances:
            await self.session.merge(instance)

    @override
    async def delete(self, *instances: Base) -> None:
        for instance in instances:
            await self.session.delete(instance)

    @override
    async def rollback(self) -> None:
        await self.session.rollback()
