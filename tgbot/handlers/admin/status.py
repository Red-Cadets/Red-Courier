from aiogram import types, Dispatcher

from tgbot.config import Config
from tgbot.models.chat_tg import ChatTG


async def _handle_status(message: types.Message, config: Config) -> None:
    text = f'''
ID текущего чата: <code>{message.chat.id}</code>
ID MAIN чата: <code>{config.tg_bot.main_chat_id}</code>
ID DEV чата: <code>{config.tg_bot.dev_chat_id}</code>
'''

    chat = ChatTG(
        id=message.chat.id
    )
    await chat.send_message(text)


def register(dp: Dispatcher) -> None:
    config: Config = dp.bot.get("config")
    dp.register_message_handler(_handle_status,
                                command=config.tg_bot.commands.status,
                                is_admin=True)
