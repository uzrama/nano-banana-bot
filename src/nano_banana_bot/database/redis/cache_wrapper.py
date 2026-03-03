from collections.abc import Awaitable
from functools import wraps
from typing import Any, Callable, ParamSpec, get_type_hints

from pydantic import TypeAdapter
from redis.typing import ExpiryT
from typing_extensions import TypeVar

from nano_banana_bot.database.redis import RedisRepository
from nano_banana_bot.utils import mjson

T = TypeVar("T", bound=Any)
P = ParamSpec("P")


def redis_cache(
    prefix: str | None = None,
    ttl: ExpiryT | None = None,
) -> Callable[[Callable[P, Awaitable[T]]], Callable[P, Awaitable[T]]]:
    def decorator(func: Callable[P, Awaitable[T]]) -> Callable[P, Awaitable[T]]:
        return_type: Any = get_type_hints(func).get("return", Any)
        type_adapter: TypeAdapter[T] = TypeAdapter(return_type)

        @wraps(func)
        async def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
            self: Any = args[0]
            key: str = ":".join(
                [
                    "cache",
                    prefix or func.__name__,
                    *map(str, args[1:]),
                    *map(str, kwargs.values()),
                ]
            )

            redis = self.redis
            if isinstance(self.redis, RedisRepository):
                redis = redis.client

            cached_value: Any = await redis.get(key)

            if isinstance(cached_value, bytes):
                cached_value = cached_value.decode()

            if cached_value is not None:
                return type_adapter.validate_python(mjson.decode(cached_value))

            result: T = await func(*args, **kwargs)
            cached_result: str = mjson.encode(type_adapter.dump_python(result))
            await redis.setex(key, ttl, cached_result)
            return result

        return wrapper

    return decorator
