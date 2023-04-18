from tgbot.models.db import BaseModel, db
from asyncpg.exceptions import UniqueViolationError
from datetime import datetime


class Service(BaseModel):
    __tablename__ = "services"

    id = db.Column(db.BigInteger, primary_key=True, unique=True, nullable=False)
    updated_at = db.Column(
        db.DateTime(True),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=db.func.now(),
    )
    name = db.Column(db.String(32), unique=True)
    is_muted = db.Column(db.Boolean, nullable=False, default=False)
    

    @classmethod
    async def add(self, name):
        try:
            fixed_name = ''.join(c if c.isalnum() else '-' for c in name)
            service = Service(name=fixed_name)
            return await service.create()
        except UniqueViolationError:
            pass


    @classmethod
    async def get(self, name):
        return await Service.query.where(Service.name == name).gino.first()


    @classmethod
    async def all(self):
        return await Service.query.gino.all()


    @classmethod
    async def clear(self):
        await Service.delete.gino.status()


    @classmethod
    async def mute(self, name):
        await self.update.values(is_muted=True).where(self.name == name).gino.status()
        

    @classmethod
    async def unmute(self, name):
        await Service.update.values(is_muted=False).where(self.name == name).gino.status()

    
    @classmethod
    async def mute_latest(self):
        last_modified_service = await Service.query.where(Service.is_muted == False).order_by(Service.updated_at.desc()).gino.first()
        if last_modified_service:
            await self.mute(last_modified_service.name)
            return last_modified_service.name


    @classmethod
    async def unmute_latest(self):
        last_modified_service = await Service.query.where(Service.is_muted == True).order_by(Service.updated_at.desc()).gino.first()
        if last_modified_service:
            await self.unmute(last_modified_service.name)
            return last_modified_service.name