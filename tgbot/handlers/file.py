from aiogram import types, Dispatcher

from tgbot.config import Config
from tgbot.storage import get_storage_client
import uuid


async def _on_document(message: types.Message, config: Config) -> None:
    document = message.document
    
    # Download the file from Telegram
    file = await message.bot.get_file(document.file_id)
    file_data = await message.bot.download_file_by_id(file.file_id)
    
    mc = get_storage_client()
    
    # Check if the bucket exists; if not, create it
    if not mc.bucket_exists(config.storage.bucket):
        mc.make_bucket(config.storage.bucket)
    
    # Save the file to Minio S3
    file_name = f"{uuid.uuid4()}_{document.file_name}"
    mc.put_object(
        config.storage.bucket, file_name, file_data, length=document.file_size, content_type=document.mime_type
    )
    
    # Generate public link and reply it to the user
    presigned_url = mc.presigned_get_object(config.storage.bucket, file_name)

    config.tg_bot.main_chat_id = message.chat.id
    text = f"Файл успешно загружен. Ваша публичная ссылка:\n{presigned_url}"
    
    await message.reply(text)


def register(dp: Dispatcher) -> None:
    config: Config = dp.bot.get("config")
    if config.storage.is_enabled:
        dp.register_message_handler(_on_document, content_types=types.ContentType.DOCUMENT)

