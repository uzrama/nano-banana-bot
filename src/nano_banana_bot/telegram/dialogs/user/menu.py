from aiogram.enums import ContentType
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Start
from aiogram_dialog.widgets.media import StaticMedia

from nano_banana_bot.telegram.dialogs.extra.i18n import I18nFormat
from nano_banana_bot.telegram.states.dialogs import GenerateSG, MenuSG

menu_window = Window(
    StaticMedia(url="https://images.unsplash.com/photo-1620641788421-7a1c342ea42e?auto=format&fit=crop&w=800&q=80", type=ContentType.PHOTO),
    I18nFormat("menu-title"),
    Start(I18nFormat("menu-btn_generating"), id="generating", state=GenerateSG.main),
    Button(I18nFormat("menu-btn_prompts"), id="menu"),
    Button(I18nFormat("menu-btn_settings"), id="menu_settings"),
    state=MenuSG.main,
)

dialog = Dialog(
    menu_window,
)
