import os
from typing import TypeVar

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

TypeModel = TypeVar("TypeModel")


class PhotoRepository:
    async def upload_photo(self, instance: TypeModel, photo: UploadFile, session: AsyncSession) -> TypeModel:
        cls = type(instance)
        if instance.avatar and os.path.exists(instance.avatar):
            os.remove(instance.avatar)
        photo_path = os.path.join("media", cls.__name__.lower(), instance.username, photo.filename)
        if not os.path.exists(os.path.dirname(photo_path)):
            os.makedirs(os.path.dirname(photo_path))
        with open(photo_path, "wb") as buffer:
            buffer.write(await photo.read())
        instance.avatar = photo_path
        return await self.update(instance=instance, session=session)

    def download_photo(self, instance: TypeModel):
        if instance.avatar and os.path.exists(instance.avatar):
            return instance.avatar

    def delete_photo(self, instance: TypeModel):
        if instance.avatar and os.path.exists(instance.avatar):
            os.remove(instance.avatar)
