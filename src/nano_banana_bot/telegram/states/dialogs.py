from typing import final
from aiogram.fsm.state import StatesGroup, State


@final
class StartSG(StatesGroup):
    main = State()


@final
class MenuSG(StatesGroup):
    main = State()


@final
class GenerateSG(StatesGroup):
    main = State()
    preview = State()
    edit_photo = State()
    edit_prompt = State()
