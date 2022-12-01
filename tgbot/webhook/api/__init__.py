from fastapi import APIRouter

from tgbot.webhook.api import webhook

wh_router = APIRouter(redirect_slashes=True)
wh_router.include_router(webhook.router)