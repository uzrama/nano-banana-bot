from types import TracebackType
from typing import override

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from nano_banana_bot.database.alchemy.repositories.general import Repository
from nano_banana_bot.database.base import BaseSessionContext

from .uow import UoW


class AlchemySessionContext(BaseSessionContext):
    _session_pool: async_sessionmaker[AsyncSession]
    _session: AsyncSession | None

    __slots__ = ("_session_pool", "_session")

    def __init__(self, session_pool: async_sessionmaker[AsyncSession]) -> None:
        self._session_pool = session_pool
        self._session = None

    @override
    async def __aenter__(self) -> tuple[Repository, UoW]:
        self._session = self._session_pool()
        return Repository(session=self._session), UoW(session=self._session)

    @override
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        if self._session is None:
            return

        try:
            if exc_type:
                # Если возникло исключение, откатываем изменения
                await self._session.rollback()
        finally:
            # В любом случае закрываем сессию
            await self._session.close()
            self._session = None
