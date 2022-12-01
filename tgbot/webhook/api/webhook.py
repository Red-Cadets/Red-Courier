from fastapi import APIRouter
from tgbot.config import Config
from tgbot.webhook.schemas import WebhookRequest
from tgbot.models.chat_tg import ChatTG

router = APIRouter()

@router.get('/')
async def check_webhook_key():
    return {'ok': True}

@router.post('/')
async def process_webhook_request(wh_request: WebhookRequest):
    chat = ChatTG()
    recv = chat.receiver(to=wh_request.to)
    chat = await ChatTG.get(recv)
    if chat is None:
        chat = ChatTG(
            id=recv
        )
        await chat.create()

    await chat.send_message(wh_request.message)