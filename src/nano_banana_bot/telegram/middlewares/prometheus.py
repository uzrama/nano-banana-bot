from collections.abc import Awaitable
import time
from typing import Any, Callable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from prometheus_client import Counter, Histogram

UPDATE_COUNTER = Counter("bot_updates_total", "Total updates received", ["update_type"])
PROCESSING_TIME = Histogram(
    "bot_processing_time_seconds",
    "Update processing time",
    ["update_type"],
    buckets=(0.05, 0.1, 0.15, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.5, 2.0, 5.0),
)
ERROR_COUNTER = Counter("bot_errors_total", "Total errors in handlers", ["update_type"])


class PrometheusMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        update_type = event.__class__.__name__
        UPDATE_COUNTER.labels(update_type=update_type).inc()
        start_time = time.perf_counter()
        try:
            result = await handler(event, data)
            return result
        except Exception:
            ERROR_COUNTER.labels(update_type=update_type).inc()
            raise
        finally:
            PROCESSING_TIME.labels(update_type=update_type).observe(time.perf_counter() - start_time)
