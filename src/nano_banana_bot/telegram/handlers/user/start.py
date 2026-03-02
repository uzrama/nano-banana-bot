from typing import TYPE_CHECKING, Any, Final

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_i18n import I18nContext


if TYPE_CHECKING:
    from nano_banana_bot.schemas.user import UserScheme

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart())
async def greeting(
    message: Message,
    i18n: I18nContext,
    user: UserScheme,
) -> Any:
    return await message.answer(f"Hello {user.name}")
