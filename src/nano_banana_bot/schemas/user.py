from datetime import datetime

from aiogram import html
from aiogram.utils.link import create_tg_link

from .base import ActiveRecordModel


class UserScheme(ActiveRecordModel):
    id: int
    name: str
    language: str
    language_code: str | None = None
    bot_blocked: bool = False
    blocked_at: datetime | None = None

    @property
    def url(self) -> str:
        return create_tg_link("user", id=self.id)

    @property
    def mention(self) -> str:
        return html.link(value=self.name, link=self.url)
