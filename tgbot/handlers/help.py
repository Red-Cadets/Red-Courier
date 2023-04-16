from aiogram import types, Dispatcher

from tgbot.config import Config
from tgbot.models.chat_tg import ChatTG


async def _handle_help(message: types.Message, config: Config) -> None:
    commands_data = ""
    for cmd in config.tg_bot.commands:
        commands_data += f"/{cmd.command} - {cmd.description}"
        if cmd.is_admin:
            commands_data += " 🔐"
        commands_data += "\n"
        
    text = f'''
Доступные команды:
{commands_data}
'''

    chat = ChatTG(
        id=message.chat.id
    )

    config.tg_bot.main_chat_id = message.chat.id
    await chat.send_message(text)



def register(dp: Dispatcher) -> None:
    config: Config = dp.bot.get("config")
    dp.register_message_handler(_handle_help,
                                command=config.tg_bot.commands.help)

