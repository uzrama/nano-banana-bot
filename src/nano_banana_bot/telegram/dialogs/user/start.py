from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.media import StaticMedia

from nano_banana_bot.telegram.dialogs.extra.i18n import I18nFormat
from nano_banana_bot.telegram.states.dialogs import MenuSG, StartSG

start_window = Window(
    StaticMedia(url="https://images.unsplash.com/photo-1677442136019-21780ecad995?auto=format&fit=crop&w=800&q=80", type=ContentType.PHOTO),
    I18nFormat("start-welcome"),
    Start(I18nFormat("start-btn_next"), id="menu", state=MenuSG.main),
    state=StartSG.main,
)

dialog = Dialog(
    start_window,
)
