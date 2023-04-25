from fastapi import APIRouter, UploadFile
from tgbot.config import get_config
from tgbot.webhook.schemas import WebhookRequest
from tgbot.models.chat_tg import ChatTG
from tgbot.models.service import Service
from tgbot.storage import get_storage_client
from os.path import getsize
import uuid

router = APIRouter()

config = get_config()

@router.post(f'/files/{config.wh.key}')
@router.post(f'/files/{config.wh.key}/')
async def upload_file(file: UploadFile):
    mc = get_storage_client()
    
    # Check if the bucket exists; if not, create it
    if not mc.bucket_exists(config.storage.bucket):
        mc.make_bucket(config.storage.bucket)
    
    # Save the file to Minio S3
    file_name = f"{uuid.uuid4()}_{file.filename}"
    mc.put_object(
        config.storage.bucket, file_name, file.file, file.size
    )
    
    # Generate public link and reply it to the user
    presigned_url = mc.presigned_get_object(config.storage.bucket, file_name)
    
    return {'link': presigned_url}
    

@router.get(f'/{config.wh.key}')
@router.get(f'/{config.wh.key}/')
async def check_webhook_key():
    return {'ok': True}

@router.post(f'/{config.wh.key}')
@router.post(f'/{config.wh.key}/')
async def process_webhook_request(wh_request: WebhookRequest):
    # add service from request
    if wh_request.id != "":
        await Service.add(wh_request.id)
    
    # add chat
    chat = ChatTG()
    recv = chat.receiver(to=wh_request.to)
    chat = await ChatTG.get(recv)
    if chat is None:
        chat = ChatTG(
            id=recv
        )
        await chat.create()

    if wh_request.id != "":
        service = await Service.get(wh_request.id)
        if service.is_muted:
            return

    await chat.send_message(wh_request.message)