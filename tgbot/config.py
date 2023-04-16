from dataclasses import dataclass, fields
from datetime import time, timedelta, datetime
from typing import List, Optional, Generator

from aiogram.types import BotCommand
from environs import Env
import os


@dataclass
class CommandInfo:
    command: str
    description: str
    alias: Optional[str] = None
    is_admin: bool = False
    bot_command: Optional[BotCommand] = None

    def __post_init__(self) -> None:
        self.bot_command = BotCommand(self.command, self.description)


@dataclass
class Commands:
    help: CommandInfo
    send_all: CommandInfo
    ping: CommandInfo
    status: CommandInfo
    init_main: CommandInfo
    init_dev: CommandInfo

    def __iter__(self) -> Generator[CommandInfo, None, None]:
        return (getattr(self, field.name) for field in fields(self))


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str
    port: int
    uri: str = ""

    def __post_init__(self) -> None:
        self.uri = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"


@dataclass
class RedisConfig:
    host: str
    port: int
    password: str
    pool_size: int


@dataclass
class TgBot:
    token: str
    admin_ids: List[int]
    use_redis: bool
    commands: Commands
    subscription_channels_ids: List[int]
    main_chat_id: str
    dev_chat_id: str


@dataclass
class WebhookServer:
    port: int
    key: str
    debug: bool
    url: str


@dataclass
class LogConfig:
    file_name: str
    rotation: time
    retention: timedelta


@dataclass
class Miscellaneous:
    pass


@dataclass
class Config:
    tg_bot: TgBot
    wh: WebhookServer
    db: DbConfig
    redis: RedisConfig
    log: LogConfig
    misc: Miscellaneous


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
            main_chat_id=env.str("MAIN_CHAT"),
            dev_chat_id=env.str("DEV_CHAT"),
            subscription_channels_ids=list(map(int, env.list("SUBSCRIPTION_CHANNELS_IDS"))),
            commands=Commands(
                help=CommandInfo("help", "Справка"),
                send_all=CommandInfo("send_all", "Рассылка", is_admin=True),
                ping=CommandInfo("ping", "Пинг", is_admin=True),
                status=CommandInfo("status", "Статус", is_admin=True),
                init_main=CommandInfo("init_main", "Установить MAIN ID", is_admin=True),
                init_dev=CommandInfo("init_dev", "Установить DEV ID", is_admin=True),
            ),
        ),
        wh=WebhookServer(
            port=env.int('WH_PORT'),
            key=env.str('WH_KEY'),
            debug=env.bool("WH_DEBUG"),
            url=env.str("WH_URL"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME'),
            port=env.int('DB_PORT'),
        ),
        redis=RedisConfig(
            host=env.str('REDIS_HOST'),
            password=env.str('REDIS_PASS'),
            port=env.int('REDIS_PORT'),
            pool_size=env.int('REDIS_POOL_SIZE'),
        ),
        log=LogConfig(
            file_name=env.str('LOG_FILE_NAME'),
            rotation=datetime.strptime(env.str('LOG_ROTATION'), '%H:%M').time(),
            retention=timedelta(days=env.int('LOG_RETENTION')),
        ),
        misc=Miscellaneous()
    )

def get_config() -> Config:
    if os.getenv('MODE') == 'DEV':
        return load_config(".env.dev")
    else:
        return load_config(".env")