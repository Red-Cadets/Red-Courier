from fastapi import APIRouter
from tgbot.config import get_config
from tgbot.webhook.schemas import WebhookRequest
from tgbot.models.chat_tg import ChatTG
from tgbot.models.service import Service

router = APIRouter()

config = get_config()

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