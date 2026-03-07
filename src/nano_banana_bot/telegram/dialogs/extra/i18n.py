from typing import Any, final

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.text import Text
from aiogram_i18n.context import I18nContext


@final
class I18nFormat(Text):
    def __init__(self, key: str, **kwargs: Any) -> None:
        super().__init__()
        self.key = key
        self.kwargs = kwargs

    async def _render_text(self, data: dict[str, Any], manager: DialogManager) -> str:
        i18n: I18nContext | None = manager.middleware_data.get("i18n")

        if i18n is None:
            return f"<{self.key}>"

        format_data = data.copy()
        format_data.update(self.kwargs)

        return i18n.get(self.key, **format_data)
