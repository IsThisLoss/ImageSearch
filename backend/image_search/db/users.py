import typing

import motor.motor_asyncio as motor

from ..models.config import Settings
from ..models.user import User


class Users:
    def __init__(
        self,
        client: motor.AsyncIOMotorClient,
        settings: Settings,
    ):
        db = client[settings.mongodb_db]
        self.users = db[settings.mongodb_user_collection]

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

    async def find(self, username: str) -> typing.Optional[User]:
        result = await self.users.find_one(
            {'username': username},
        )
        if not result:
            return None
        return User(username=username)

    async def get_hashed_password(self, username: str) -> typing.Optional[str]:
        result = await self.users.find_one(
            {'username': username},
        )
        if not result:
            return None
        return str(result['hashed_password'])
