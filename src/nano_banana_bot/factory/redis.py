from redis.asyncio import ConnectionPool, Redis

from nano_banana_bot.config import AppConfig


def create_redis(config: AppConfig) -> Redis:
    return Redis(connection_pool=ConnectionPool.from_url(url=config.redis.build_url()))
