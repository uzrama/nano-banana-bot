from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const

from nano_banana_bot.telegram.states.dialogs import StartSG


start_window = Window(
    Const("Привет"),
    Button(Const("Далее ➡️"), id="menu"),
    state=StartSG.main,
)

dialog = Dialog(
    start_window,
)
