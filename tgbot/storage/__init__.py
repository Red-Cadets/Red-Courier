from minio import Minio
from tgbot.config import get_config

config = get_config()

def get_storage_client():
    return Minio(
    config.storage.endpoint,
    access_key=config.storage.access_key,
    secret_key=config.storage.secret_key,
    secure=True
)
