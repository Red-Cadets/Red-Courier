from pydantic import BaseModel, Field

class WebhookRequest(BaseModel):
    message: str = Field(...)
    to: str = Field(default="DEV")
    type: str = Field(default="markdown")
    service: str