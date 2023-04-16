from aiogram import Dispatcher

from tgbot.handlers import admin
from tgbot.handlers import start
from tgbot.handlers import subscription
from tgbot.handlers import help


def register(dp: Dispatcher) -> None:
    admin.register(dp)
    start.register(dp)
    subscription.register(dp)
    help.register(dp)
