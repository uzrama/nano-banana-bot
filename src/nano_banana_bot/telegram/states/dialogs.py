from typing import final
from aiogram.fsm.state import StatesGroup, State


@final
class StartSG(StatesGroup):
    main = State()
