from pydantic.types import SecretStr
from nano_banana_bot.config.env.base import EnvSettings


class TelegramConfig(EnvSettings, env_prefix="TELEGRAM_"):
    bot_token: SecretStr
    webhook_secret: SecretStr
    drop_pending_updates: bool
    use_webhook: bool
    reset_webhook: bool
    webhook_path: str
