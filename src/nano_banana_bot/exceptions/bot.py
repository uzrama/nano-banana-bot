from .base import AppError


class BotError(AppError):
    pass


class UnknownMessageError(BotError):
    pass
