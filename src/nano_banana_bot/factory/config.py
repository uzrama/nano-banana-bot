from nano_banana_bot.config.env import (
    AppConfig,
    CommonConfig,
    PostgresConfig,
    RedisConfig,
    ServerConfig,
    SQLAlchemyConfig,
    TelegramConfig,
)


def create_app_config() -> AppConfig:
    return AppConfig(
        telegram=TelegramConfig(),
        postgres=PostgresConfig(),
        alchemy=SQLAlchemyConfig(),
        redis=RedisConfig(),
        server=ServerConfig(),
        common=CommonConfig(),
    )
