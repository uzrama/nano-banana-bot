from typing import Any, cast, override

from sqlalchemy import ColumnExpressionArgument, delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from nano_banana_bot.database.base import BaseRepository


class BaseAlchemyRepository[M](BaseRepository[M, ColumnExpressionArgument[bool]]):
    session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    @override
    async def _get(self, model: type[M], *conditions: ColumnExpressionArgument[bool]) -> M | None:
        return await self.session.scalar(select(model).where(*conditions))

    @override
    async def _get_many(
        self,
        model: type[M],
        *conditions: ColumnExpressionArgument[bool],
    ) -> list[M]:
        return list(await self.session.scalars(select(model).where(*conditions)))

    @override
    async def _update(
        self,
        model: type[M],
        *conditions: ColumnExpressionArgument[bool],
        load_result: bool = True,
        **kwargs: Any,
    ) -> M | None:
        if not kwargs:
            if not load_result:
                return None
            return cast(M, await self._get(model, *conditions))
        query = update(model).where(*conditions).values(**kwargs)
        if load_result:
            query = query.returning(model)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() if load_result else None

    @override
    async def _delete(
        self,
        model: type[M],
        *conditions: ColumnExpressionArgument[bool],
    ) -> bool:
        result = await self.session.execute(delete(model).where(*conditions))
        return cast(bool, result.rowcount > 0)  # pyright: ignore[reportAttributeAccessIssue]
