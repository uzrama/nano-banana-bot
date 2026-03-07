from typing import Final

from aiogram import Router

from .user import start, menu, generate


user_dialogs: Final[Router] = Router(name=__name__)

user_dialogs.include_routers(start.dialog, menu.dialog, generate.dialog)
