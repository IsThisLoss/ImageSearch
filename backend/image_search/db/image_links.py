import typing
import datetime
import dataclasses

from bson import ObjectId
import dacite
import motor.motor_asyncio as motor

from . import utils
from ..models.config import Settings

# DTOs

@dataclasses.dataclass
class ImagePreview:
    medium: str


@dataclasses.dataclass
class ImageLink:
    id: typing.Optional[str]
    orig: str
    previews: ImagePreview
    ts: int = dataclasses.field(default_factory=utils.now)

    def as_dict(self):
        return utils.as_dict(self)


# DAO

class ImageLinks:
    COLLECTION_NAME = 'image_links'

    def __init__(
        self,
        client: motor.AsyncIOMotorClient,
        settings: Settings,
    ):
        db = client[settings.mongodb_db]
        self._image_links = db[self.COLLECTION_NAME]

    @staticmethod
    def to_model_id(data: dict):
        data['id'] = str(data.pop('_id'))
        return data

    async def get(self, id: str) -> typing.Optional[ImageLink]:
        data = await self._image_links.find_one(
            {
                '_id': ObjectId(id),
            },
        )
        if not data:
            return None
        return dacite.from_dict(
            data_class=ImageLink,
            data=self.to_model_id(data),
        )

    async def put(self, image_link: ImageLink) -> str:
        data = image_link.as_dict()
        result = await self._image_links.insert_one(data)
        return str(result.inserted_id)

    async def delete(self, id: str):
        await self._image_links.delete_many(
            {'_id': ObjectId(id)},
        )

    async def delete_many(self, ids: typing.List[str]):
        obj_ids = list(map(ObjectId, ids))
        await self._image_links.delete_many(
            {'_id': {'$in': obj_ids}},
        )

    async def find_older_than(self, ts: int) -> typing.List[ImageLink]:
        data = self._image_links.find(
            {'ts': {'$lt': ts}},
        )
        result = []
        async for item in data:
            result.append(dacite.from_dict(
                data_class=ImageLink,
                data=self.to_model_id(item),
            ))
        return result
