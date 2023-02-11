import typing
from functools import lru_cache

from . import mongo
from ..models.config import Settings, get_config
from ..models import user


class Users:
    def __init__(self):
        client = mongo.get_client()
        config: Settings = get_config()
        db = client[config.mongodb_db]
        self.users = db[config.mongodb_user_collection]

    async def put(self, username: str, hashed_password: str):
        data = {
            'username': username,
            'hashed_password': hashed_password,
        }
        await self.users.find_one_and_update(
            {'username': username},
            {'$setOnInsert': data},
            new=True,
            upsert=True,
        )

    async def find(self, username: str) -> typing.Optional[user.User]:
        result = await self.users.find_one(
            {'username': username},
        )
        if not result:
            return None
        return user.User(username=username)

    async def get_hashed_password(self, username: str) -> typing.Optional[str]:
        result = await self.users.find_one(
            {'username': username},
        )
        if not result:
            return None
        return str(result['hashed_password'])


@lru_cache()
def get_users() -> Users:
    return Users()
