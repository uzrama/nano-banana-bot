from typing import Final

from aiogram import Router

from .user import start

user_handlers: Final[Router] = Router(name=__name__)

user_handlers.include_routers(start.router)
