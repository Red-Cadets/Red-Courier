from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.types import Update
from uvicorn import run
from loguru import logger

from tgbot.config import get_config
from tgbot import filters
from tgbot import handlers
from tgbot import middlewares
from tgbot.misc import logging
from tgbot.models import db
from tgbot.models.user_tg import UserTG
from tgbot.models.chat_tg import ChatTG
from tgbot.services.broadcasting import send_to_admins
from tgbot.services.setting_commands import set_bot_command

from fastapi import FastAPI
from typing import Dict
from tgbot.webhook.api import wh_router

config = get_config()

logging.setup(config.log.file_name, config.log.rotation, config.log.retention)

if config.tg_bot.use_redis:
    storage = RedisStorage2(host=config.redis.host,
                            port=config.redis.port,
                            password=config.redis.password,
                            pool_size=config.redis.pool_size)
else:
    storage = MemoryStorage()

bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
bot['config'] = config
dp = Dispatcher(bot, storage=storage)

app = FastAPI()

app.include_router(wh_router, tags=["webhook"])

WEBHOOK_URL = f'{config.wh.url}/bot/{config.tg_bot.token}'

@app.post(f"/bot/{config.tg_bot.token}")
async def bot_webhook(update: Dict):
    updater = Update(**update)
    Dispatcher.set_current(dp)
    Bot.set_current(bot)
    try:
        await dp.process_update(updater)
        return {"ok": True}
    except Exception as e:
        logger.error(e)
        return {"ok": False}

@app.on_event("startup")
async def on_startup():
    logger.info("Starting bot")

    await db.on_startup(config.db.uri)
    UserTG.bot = bot
    ChatTG.bot = bot

    wh_info = await bot.get_webhook_info()
    if wh_info.url != WEBHOOK_URL:
        await bot.set_webhook(url=WEBHOOK_URL)

    await middlewares.register(dp, config)
    filters.register(dp)
    handlers.register(dp)

    await set_bot_command(bot, config)
    await send_to_admins(bot, "Бот запущен")


@app.on_event("shutdown")
async def on_shutdown():
    logger.info("Shutting down bot")

    await dp.storage.close()
    await dp.storage.wait_closed()
    await (await bot.get_session()).close()
    await db.on_shutdown()

if __name__ == '__main__':
    try:
        run("bot:app", host="0.0.0.0", port=config.wh.port, reload=config.wh.debug)
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
        raise SystemExit(0)
