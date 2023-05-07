import typing
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
    ts: int = utils.now()

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
