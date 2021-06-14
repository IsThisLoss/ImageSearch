from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import TEXT

from functools import lru_cache
from ..models.config import Settings, get_config


@lru_cache()
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
    images = db[config.mongodb_image_collection]
    await images.create_index([
        ('title', TEXT),
        ('description', TEXT),
        ('cv_text', TEXT),
    ])
    await images.create_index('url', unique=True)
