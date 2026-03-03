from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any


class BaseUnitOfWork[M](ABC):
    @abstractmethod
    async def commit(self, *instances: M) -> None: ...

    @abstractmethod
    async def merge(self, *instances: M) -> None: ...

    @abstractmethod
    async def delete(self, *instances: M) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...


class BaseSessionContext[R: BaseRepository[Any, Any], U: BaseUnitOfWork[Any]](ABC):
    @abstractmethod
    async def __aenter__(self) -> tuple[R, U]: ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...


class BaseRepository[M, C](ABC):
    @abstractmethod
    async def _get(self, model: type[M], *conditions: C) -> M | None: ...

    @abstractmethod
    async def _get_many(self, model: type[M], *conditions: C) -> list[M]: ...

    @abstractmethod
    async def _update(self, model: type[M], *conditions: C, load_result: bool = True, **kwargs: Any) -> M | None: ...

    @abstractmethod
    async def _delete(self, model: type[M], *conditions: C) -> bool: ...
