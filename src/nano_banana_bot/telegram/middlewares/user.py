from collections.abc import Awaitable
import logging
from typing import TYPE_CHECKING, Any, Callable, Final

from aiogram.types import TelegramObject
from aiogram.types import User as AiogramUser
from aiogram_i18n import I18nMiddleware

from nano_banana_bot.services.crud.user import UserService
from nano_banana_bot.telegram.middlewares.event_typed import EventTypedMiddleware

if TYPE_CHECKING:
    from nano_banana_bot.schemas.user import UserScheme

logger: Final[logging.Logger] = logging.getLogger(__name__)


class UserMiddleware(EventTypedMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any | None:
        aiogram_user: AiogramUser | None = data.get("event_from_user")
        if aiogram_user is None or aiogram_user.is_bot:
            # Prevents the bot itself from being added to the database
            # when accepting chat_join_request and receiving chat_member updates.
            return await handler(event, data)

        user_service: UserService = data["user_service"]
        user: UserScheme | None = await user_service.get(user_id=aiogram_user.id)
        if user is None:
            i18n: I18nMiddleware = data["i18n_middleware"]
            user = await user_service.create(aiogram_user=aiogram_user, i18n_core=i18n.core)
            logger.info(
                "New user in database: %s (%d)",
                aiogram_user.full_name,
                aiogram_user.id,
            )

        data["user"] = user
        return await handler(event, data)
