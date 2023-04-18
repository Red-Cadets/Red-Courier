from aiogram import types, Dispatcher

from tgbot.config import Config
from tgbot.models.chat_tg import ChatTG
from tgbot.models.service import Service


async def _handle_mute_latest(message: types.Message, config: Config) -> None:
    service_name = await Service.mute_latest()
    
    if service_name:
        text = f'Сервис [{service_name}] отключен 🤐'
    else:
        text = 'Все сервисы заглушены'

    chat = ChatTG(
        id=message.chat.id
    )
    await chat.send_message(text)


async def _handle_unmute_latest(message: types.Message, config: Config) -> None:
    service_name = await Service.unmute_latest()
    
    if service_name:
        text = f'Сервис [{service_name}] включен'
    else:
        text = 'Все сервисы включены'

    chat = ChatTG(
        id=message.chat.id
    )
    await chat.send_message(text)


async def _handle_services(message: types.Message, config: Config) -> None:
    services = await Service.all()
    if services:
        services_text = ""
        for service in services:
            services_text += service.name
            if service.is_muted:
                services_text += ' (отключен 🤐)'
            services_text +=  '\n'
        
        text = f'''
Сервисы:
{services_text}
'''
    else:
        text = 'Сервисы отсутствуют'

    chat = ChatTG(
        id=message.chat.id
    )
    await chat.send_message(text)

def register(dp: Dispatcher) -> None:
    config: Config = dp.bot.get("config")
    dp.register_message_handler(_handle_mute_latest,
                                command=config.tg_bot.commands.mute_latest,
                                is_admin=True)
    dp.register_message_handler(_handle_unmute_latest,
                                command=config.tg_bot.commands.unmute_latest,
                                is_admin=True)
    dp.register_message_handler(_handle_services,
                                command=config.tg_bot.commands.services,
                                is_admin=True)
