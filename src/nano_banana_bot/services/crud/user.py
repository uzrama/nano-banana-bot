from typing import Any

from aiogram.types import User as AiogramUser
from aiogram_i18n.cores import BaseCore

from nano_banana_bot.const import DEFAULT_LOCALE, TIME_1M
from nano_banana_bot.database.alchemy import AlchemySessionContext
from nano_banana_bot.database.redis.cache_wrapper import redis_cache
from nano_banana_bot.models.user import User
from nano_banana_bot.schemas.user import UserScheme
from nano_banana_bot.services.crud.base import CrudService
from nano_banana_bot.utils.key_builder import build_key


class UserService(CrudService):
    async def clear_cache(self, user_id: int) -> None:
        cache_key: str = build_key("cache", "get_user", user_id=user_id)
        await self.redis.delete(cache_key)

    async def create(self, aiogram_user: AiogramUser, i18n_core: BaseCore[Any]) -> UserScheme:
        db_user: User = User(
            id=aiogram_user.id,
            name=aiogram_user.full_name,
            language=(aiogram_user.language_code if aiogram_user.language_code in i18n_core.available_locales else DEFAULT_LOCALE),
            language_code=aiogram_user.language_code,
        )

        async with AlchemySessionContext(session_pool=self.session_pool) as (_, uow):
            await uow.commit(db_user)

        await self.clear_cache(user_id=aiogram_user.id)
        return db_user.scheme()

    @redis_cache(prefix="get_user", ttl=TIME_1M)
    async def get(self, user_id: int) -> UserScheme | None:
        async with AlchemySessionContext(session_pool=self.session_pool) as (repository, _):
            user = await repository.users.get(user_id=user_id)
            if user is None:
                return None
            return user.scheme()

    async def count(self) -> int:
        async with AlchemySessionContext(session_pool=self.session_pool) as (repository, _):
            return await repository.users.count()

    async def update(self, user: UserScheme, **data: Any) -> UserScheme | None:
        async with AlchemySessionContext(session_pool=self.session_pool) as (repository, uow):
            for key, value in data.items():
                setattr(user, key, value)
            user_db = await repository.users.update(user_id=user.id, **user.model_state)
            if user_db is None:
                return None
            await uow.commit()

            await self.clear_cache(user_id=user.id)
            return user_db.scheme()
