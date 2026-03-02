from typing import Any, TypedDict

from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from nano_banana_bot.config import AppConfig
from nano_banana_bot.services.crud import UserService
from nano_banana_bot.database.redis import RedisRepository


class Services(TypedDict):
    redis_repository: RedisRepository
    user_service: UserService


def create_services(
    session_pool: async_sessionmaker[AsyncSession],
    redis: Redis,
    config: AppConfig,
) -> Services:
    crud_service_kwargs: dict[str, Any] = {
        "session_pool": session_pool,
        "redis": redis,
        "config": config,
    }

    redis_repository: RedisRepository = RedisRepository(client=redis, config=config)
    user_service: UserService = UserService(**crud_service_kwargs)

    return Services(redis_repository=redis_repository, user_service=user_service)
