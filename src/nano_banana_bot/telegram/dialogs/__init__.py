from typing import Final

from aiogram import Router

from .user import start


user_dialogs: Final[Router] = Router(name=__name__)

user_dialogs.include_routers(start.dialog)
