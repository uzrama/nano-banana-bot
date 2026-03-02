from aiogram import Bot, Dispatcher

from nano_banana_bot.factory import create_app_config, create_bot, create_dispatcher
from nano_banana_bot.config import AppConfig
from nano_banana_bot.runners import run_polling, run_webhook


def main() -> None:
    config: AppConfig = create_app_config()
    bot: Bot = create_bot(config=config)
    dispatcher: Dispatcher = create_dispatcher(config=config)
    if config.telegram.use_webhook:
        return run_webhook(dispatcher=dispatcher, bot=bot, config=config)
    return run_polling(dispatcher=dispatcher, bot=bot, config=config)


if __name__ == "__main__":
    main()
