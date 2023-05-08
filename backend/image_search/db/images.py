import typing
import dataclasses

from bson import ObjectId
import dacite
import motor.motor_asyncio as motor
import pymongo

from . import utils
from ..models.config import Settings


# DTOs

@dataclasses.dataclass
class ImagePreview:
    medium: str


@dataclasses.dataclass
class ImageLinks:
    orig: str
    previews: ImagePreview


@dataclasses.dataclass
class Image:
    id: typing.Optional[str]
    username: str
    title: str
    description: str
    links: ImageLinks
    cv_text: typing.Optional[str] = None
    ts: int = dataclasses.field(default_factory=utils.now)

    def as_dict(self):
        return utils.as_dict(self)

# DAO

class Images:
    COLLECTION_NAME = 'images'

    def __init__(
        self,
        client: motor.AsyncIOMotorClient,
        settings: Settings,
    ):
        db = client[settings.mongodb_db]
        self.images = db[self.COLLECTION_NAME]

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
        condition: typing.Dict[str, typing.Any] = {'username': username}
        if text:
            condition['$text'] = {'$search': text}

        cursor = self.images.find(
            condition,
        ).sort(
            (
                ('ts', pymongo.DESCENDING),
                ('_id', pymongo.DESCENDING),
            )
        ).skip(offset).limit(limit)

        result = []
        async for entry in cursor:
            result.append(
                dacite.from_dict(
                    data_class=Image,
                    data=self.to_model_id(entry),
                ),
            )

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
        return dacite.from_dict(
            data_class=Image,
            data=self.to_model_id(data),
        )

    async def put(self, username: str, image: Image) -> str:
        data: dict = image.as_dict()
        result = await self.images.find_one_and_replace(
            {'username': username, 'links.orig': image.links.orig},
            data,
            upsert=True,
            new=True,
        )
        return str(result['_id'])

    async def update(self, username: str, image: Image) -> bool:
        image.ts = utils.now()
        data = image.as_dict()
        result = await self.images.update_one(
            {'_id': ObjectId(image.id), 'username': username},
            {'$set': data},
        )
        return result.modified_count > 0

    async def delete(self, username: str, id: str):
        await self.images.delete_many(
            {'_id': ObjectId(id), 'username': username},
        )
