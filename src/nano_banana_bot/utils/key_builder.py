from enum import Enum
from typing import TYPE_CHECKING, Any, ClassVar
from uuid import UUID

from pydantic import BaseModel


def build_key(prefix: str, /, *parts: Any, **kw_parts: Any) -> str:
    return ":".join([prefix, *map(str, parts), *map(str, kw_parts.values())])


class StorageKey(BaseModel):
    if TYPE_CHECKING:
        __separator__: ClassVar[str]
        """Data separator (default is :code:`:`)"""
        __prefix__: ClassVar[str | None]
        """Storage key prefix"""

    def __init_subclass__(cls, **kwargs: Any) -> None:
        cls.__separator__ = kwargs.pop("separator", ":")
        cls.__prefix__ = kwargs.pop("prefix", None)
        if cls.__separator__ in (cls.__prefix__ or ""):
            raise ValueError(f"Separator symbol {cls.__separator__!r} can not be used inside prefix {cls.__prefix__!r}")
        super().__init_subclass__(**kwargs)

    @classmethod
    def encode_value(cls, value: Any) -> str:
        if value is None:
            return "null"
        if isinstance(value, Enum):
            return str(value.value)
        if isinstance(value, UUID):
            return value.hex
        if isinstance(value, bool):
            return str(int(value))
        return str(value)

    def pack(self) -> str:
        result = [self.__prefix__] if self.__prefix__ else []
        for key, value in self.model_dump(mode="json").items():
            encoded = self.encode_value(value)
            if self.__separator__ in encoded:
                raise ValueError(f"Separator symbol {self.__separator__!r} can not be used in value {key}={encoded!r}")
            result.append(encoded)
        return self.__separator__.join(result)
