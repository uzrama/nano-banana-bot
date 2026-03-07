from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from prometheus_client import make_asgi_app


def setup_fastapi(app: FastAPI, dispatcher: Dispatcher, bot: Bot) -> FastAPI:
    metrics_app = make_asgi_app()
    app.mount("/metrics", metrics_app)
    for key, value in dispatcher.workflow_data.items():
        setattr(app.state, key, value)
    app.state.dispatcher = dispatcher
    app.state.bot = bot
    app.state.shutdown_completed = False
    return app
