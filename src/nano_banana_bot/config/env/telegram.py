from pydantic.types import SecretStr

from nano_banana_bot.config.env.base import EnvSettings
from nano_banana_bot.utils.custom_types import StringList


class TelegramConfig(EnvSettings, env_prefix="TELEGRAM_"):
    bot_token: SecretStr
    webhook_secret: SecretStr
    drop_pending_updates: bool
    use_webhook: bool
    reset_webhook: bool
    locales: StringList
    webhook_path: str
