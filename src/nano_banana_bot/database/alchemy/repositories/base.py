from __future__ import annotations

from typing import Any, TypeVar, cast, override

from sqlalchemy import ColumnExpressionArgument, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from nano_banana_bot.database.base import BaseRepository

T = TypeVar("T", bound=Any)
ColumnClauseType = type[T] | InstrumentedAttribute[T]


class BaseAlchemyRepository(BaseRepository):
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @override
    async def _get(self, model: ColumnClauseType[T], *conditions: ColumnExpressionArgument[Any]) -> T | None:
        return await self.session.scalar(select(model).where(*conditions))

    @override
    async def _get_many(
        self,
        model: ColumnClauseType[T],
        *conditions: ColumnExpressionArgument[Any],
    ) -> list[T]:
        return list(await self.session.scalars(select(model).where(*conditions)))

    @override
    async def _update(
        self,
        model: ColumnClauseType[T],
        *conditions: ColumnExpressionArgument[Any],
        load_result: bool = True,
        **kwargs: Any,
    ) -> T | None:
        if not kwargs:
            if not load_result:
                return None
            return cast(T, await self._get(model, *conditions))
        query = update(model).where(*conditions).values(**kwargs)
        if load_result:
            query = query.returning(model)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() if load_result else None

    @override
    async def _delete(
        self,
        model: ColumnClauseType[T],
        *conditions: ColumnExpressionArgument[Any],
    ) -> bool:
        result = await self.session.execute(delete(model).where(*conditions))
        return cast(bool, result.rowcount > 0)
