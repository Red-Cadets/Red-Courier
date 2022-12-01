from aiogram import types, Dispatcher

from tgbot.config import Config
from tgbot.models.chat_tg import ChatTG


async def _handle_init_main(message: types.Message, config: Config) -> None:
    text = f'''
ID MAIN чата изменен: <code>{message.chat.id}</code>
'''

    chat = ChatTG(
        id=message.chat.id
    )

    config.tg_bot.main_chat_id = message.chat.id
    await chat.send_message(text)


async def _handle_init_dev(message: types.Message, config: Config) -> None:
    text = f'''
ID DEV чата изменен: <code>{message.chat.id}</code>
'''

    chat = ChatTG(
        id=message.chat.id
    )

    config.tg_bot.dev_chat_id = message.chat.id
    await chat.send_message(text)


def register(dp: Dispatcher) -> None:
    config: Config = dp.bot.get("config")
    dp.register_message_handler(_handle_init_main,
                                command=config.tg_bot.commands.init_main,
                                is_admin=True)

    dp.register_message_handler(_handle_init_dev,
                                command=config.tg_bot.commands.init_dev,
                                is_admin=True)
