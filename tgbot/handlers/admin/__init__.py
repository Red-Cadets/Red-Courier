from aiogram import Dispatcher

from tgbot.handlers.admin import send_all
from tgbot.handlers.admin import init_chats
from tgbot.handlers.admin import status
from tgbot.handlers.admin import ping


def register(dp: Dispatcher) -> None:
    send_all.register(dp)
    ping.register(dp)
    status.register(dp)
    init_chats.register(dp)
