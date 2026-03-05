from typing import Any, Final

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from aiogram_dialog import DialogManager

from nano_banana_bot.telegram.states.dialogs import StartSG


router: Final[Router] = Router(name=__name__)


@router.message(CommandStart())
async def greeting(_: Message, dialog_manager: DialogManager) -> Any:
    return await dialog_manager.start(state=StartSG.main)
