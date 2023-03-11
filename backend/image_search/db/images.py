import time
import typing

from bson import ObjectId
import pymongo
import motor.motor_asyncio as motor

from ..models.config import Settings
from ..models.image import InputImage, Image


class Images:
    def __init__(
        self,
        client: motor.AsyncIOMotorClient,
        settings: Settings,
    ):
        db = client[settings.mongodb_db]
        self.images = db[settings.mongodb_image_collection]

    @staticmethod
    def to_model_id(data: dict):
        data['id'] = str(data.pop('_id'))
        return data

    async def find(
        self,
        username: str,
        text: typing.Optional[str] = None,
        offset: int = 0,
        limit: int = 100,
    ) -> typing.List[Image]:
        condition: dict = {'username': username}
        if text:
            text_condition: dict = {'$text': {'$search': text}}
            condition.update(text_condition)

        cursor = self.images.find(
            condition,
        ).sort(
            'ts', pymongo.DESCENDING,
        ).skip(offset).limit(limit)

        result = []
        async for entry in cursor:
            result.append(Image(**self.to_model_id(entry)))

        return result

    async def get(self, username: str, id: str) -> typing.Optional[Image]:
        data = await self.images.find_one(
            {
                '_id': ObjectId(id),
                'username': username,
            },
        )
        if not data:
            return None
        return Image(**self.to_model_id(data))

    async def put(self, username: str, image: InputImage) -> str:
        url: str = image.url
        data: dict = image.dict()
        # TODO Вынести отдельно
        # TODO Распозновать текст асинхронно
        # cv_text = await get_text_from_image_url(image.url)
        # data.update({'cv_text': cv_text})
        data['ts'] = int(time.time())
        result = await self.images.find_one_and_update(
            {'url': url, 'username': username},
            {'$setOnInsert': data},
            new=True,
            upsert=True,
        )
        return str(result['_id'])

    async def update(self, username: str, id: str, image: InputImage) -> bool:
        data = image.dict()
        data['ts'] = int(time.time())
        result = await self.images.update_one(
            {'_id': ObjectId(id), 'username': username},
            {'$set': data},
        )
        return result.modified_count > 0

    async def delete(self, username: str, id: str):
        await self.images.delete_many(
            {'_id': ObjectId(id), 'username': username},
        )
