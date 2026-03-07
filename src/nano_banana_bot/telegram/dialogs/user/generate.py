from typing import cast

from aiogram.enums import ContentType
from aiogram.types import Message, PhotoSize
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Start, SwitchTo
from aiogram_dialog.widgets.media import DynamicMedia

from nano_banana_bot.telegram.dialogs.extra.i18n import I18nFormat
from nano_banana_bot.telegram.states.dialogs import GenerateSG, MenuSG


async def input_handler(message: Message, _: MessageInput, manager: DialogManager):
    dialog_data = cast(dict[str, str], manager.dialog_data)

    if message.photo is not None:
        dialog_data["photo_ref_id"] = message.photo[-1].file_id
        if message.caption:
            dialog_data["prompt"] = message.caption
    if message.text is not None:
        dialog_data["prompt"] = message.text

    await message.delete()
    await manager.switch_to(state=GenerateSG.preview, show_mode=ShowMode.EDIT)


async def get_preview_data(dialog_manager: DialogManager, **_) -> dict[str, MediaAttachment | str]:
    dialog_data = cast(dict[str, str], dialog_manager.dialog_data)

    photo_ref_id = dialog_data.get("photo_ref_id")
    prompt = dialog_data.get("prompt", "")

    if photo_ref_id:
        media = MediaAttachment(file_id=MediaId(photo_ref_id), type=ContentType.PHOTO)
    else:
        # Placeholder if no photo was uploaded (use URL as default)
        media = MediaAttachment(url="https://images.pexels.com/photos/247676/pexels-photo-247676.jpeg", type=ContentType.PHOTO)

    return {
        "photo": media,
        "prompt": prompt,
    }


async def edit_photo_handler(message: Message, _: MessageInput, manager: DialogManager):
    dialog_data = cast(dict[str, str], manager.dialog_data)
    photo = cast(list[PhotoSize], message.photo)

    photo_ref_id = photo[-1].file_id
    dialog_data["photo_ref_id"] = photo_ref_id

    if message.caption:
        dialog_data["prompt"] = message.caption

    await message.delete()
    await manager.switch_to(state=GenerateSG.preview, show_mode=ShowMode.EDIT)


async def edit_prompt_handler(message: Message, _: MessageInput, manager: DialogManager):
    dialog_data = cast(dict[str, str], manager.dialog_data)
    prompt = cast(str, message.text)

    dialog_data["prompt"] = prompt

    await message.delete()
    await manager.switch_to(state=GenerateSG.preview, show_mode=ShowMode.EDIT)


input_window = Window(
    I18nFormat("generate-input_start"),
    MessageInput(input_handler, content_types=[ContentType.TEXT, ContentType.PHOTO]),
    state=GenerateSG.main,
)

edit_photo_window = Window(
    I18nFormat("generate-input_photo"),
    MessageInput(edit_photo_handler, content_types=[ContentType.PHOTO]),
    state=GenerateSG.edit_photo,
)

edit_prompt_window = Window(
    I18nFormat("generate-input_prompt"),
    MessageInput(edit_prompt_handler, content_types=[ContentType.TEXT]),
    state=GenerateSG.edit_prompt,
)

prewiew_window = Window(
    DynamicMedia("photo"),
    I18nFormat("generate-preview_prompt"),
    SwitchTo(I18nFormat("generate-btn_edit_photo"), id="edit_photo", state=GenerateSG.edit_photo),
    SwitchTo(I18nFormat("generate-btn_edit_prompt"), id="edit_prompt", state=GenerateSG.edit_prompt),
    Button(I18nFormat("generate-btn_generate"), id="generate"),
    Start(I18nFormat("generate-btn_back"), state=MenuSG.main, id="menu"),
    state=GenerateSG.preview,
    getter=get_preview_data,
)

dialog = Dialog(input_window, prewiew_window, edit_photo_window, edit_prompt_window)
