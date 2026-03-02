from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any, TypeVar

T = TypeVar("T", bound=Any)


class BaseUnitOfWork(ABC):
    @abstractmethod
    async def commit(self, *instances: Any) -> None: ...

    @abstractmethod
    async def merge(self, *instances: Any) -> None: ...

    @abstractmethod
    async def delete(self, *instances: Any) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...


class BaseSessionContext(ABC):
    @abstractmethod
    async def __aenter__(self) -> tuple[BaseRepository, BaseUnitOfWork]: ...

    @abstractmethod
    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None: ...


class BaseRepository(ABC):
    @abstractmethod
    async def _get(self, model: Any, *conditions: Any) -> T | None: ...

    @abstractmethod
    async def _get_many(self, model: Any, *conditions: Any) -> list[T]: ...

    @abstractmethod
    async def _update(self, model: Any, *conditions: Any, load_result: bool = True, **kwargs: Any) -> T | None: ...

    @abstractmethod
    async def _delete(self, model: Any, *conditions: Any) -> bool: ...
