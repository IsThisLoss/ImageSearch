from motor.motor_asyncio import AsyncIOMotorClient
import functools
import pymongo

from .images import Images
from ..models.config import Settings, get_config


@functools.lru_cache()
def get_client():
    config: Settings = get_config()
    client = AsyncIOMotorClient(
        'mongodb://{}:{}@{}:{}/{}'.format(
            config.mongodb_login,
            config.mongodb_password,
            config.mongodb_host,
            config.mongodb_port,
            config.mongodb_db
        )
    )
    return client


async def create_indexes():
    config: Settings = get_config()
    client = get_client()
    db = client[config.mongodb_db]
    images = db[Images.COLLECTION_NAME]
    await images.create_index([
        ('title', pymongo.TEXT),
        ('description', pymongo.TEXT),
        ('cv_text', pymongo.TEXT),
    ])
    await images.create_index(
        [
            ('username', pymongo.ASCENDING),
            ('links.orig', pymongo.ASCENDING),
        ],
        unique=True,
    )
