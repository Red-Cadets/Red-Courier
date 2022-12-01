from tgbot.models.db import TimedBaseModel, db


class Chat(TimedBaseModel):
    __tablename__ = "chats"

    id = db.Column(db.BigInteger, primary_key=True, unique=True, nullable=False)
    is_private = db.Column(db.Boolean, nullable=False, default=False)
    mention = db.Column(db.String(255), nullable=True)
    link = db.Column(db.String(225), nullable=True)
