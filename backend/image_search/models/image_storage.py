from .image import InputImage, Image
from ..db import mongo
from .cv import get_text_from_image_url
from .config import Settings, get_config
from bson import ObjectId

from typing import List
from functools import lru_cache


class ImageStorage:
    def __init__(self):
        client = mongo.get_client()
        config: Settings = get_config()
        db = client[config.mongodb_db]
        self.images = db[config.mongodb_image_collection]

    @staticmethod
    def to_model_id(data: dict):
        data['id'] = str(data.pop('_id'))
        return data

    async def get_all(self) -> List[Image]:
        cursor = self.images.find()
        result = []
        async for entry in cursor:
            result.append(Image(**self.to_model_id(entry)))
        return result

    async def get(self, id: str) -> Image:
        data: dict = await self.images.find_one({'_id': ObjectId(id)})
        return Image(**self.to_model_id(data))

    async def put(self, image: InputImage) -> str:
        cv_text = await get_text_from_image_url(image.url)
        url: str = image.url
        data: dict = image.dict()
        # TODO Вынести отдельно
        # TODO Распозновать текст асинхронно
        data.update({'cv_text': cv_text})
        result = await self.images.find_one_and_update(
            {'url': url},
            {'$setOnInsert': data},
            new=True,
            upsert=True,
        )
        return str(result['_id'])

    async def update(self, id: str, image: InputImage) -> bool:
        result = await self.images.update_one(
            {'_id': ObjectId(id)},
            {'$set': image.dict()},
        )
        return result.modified_count > 0

    async def delete(self, id: str):
        await self.images.delete_many({'_id': ObjectId(id)})

    async def search(self, text: str) -> List[Image]:
        cursor = self.images.find(
            {
                '$text': {
                    '$search': text
                }
            }
        )
        result = []
        async for entry in cursor:
            result.append(Image(**self.to_model_id(entry)))
        return result


@lru_cache()
def get_image_storage() -> ImageStorage:
    return ImageStorage()
