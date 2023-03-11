import functools
import dataclasses

from . import mongo
from .images import Images
from .users import Users

from ..models.config import get_config


@dataclasses.dataclass
class Database:
    images: Images
    users: Users


@functools.lru_cache()
def get_db():
    settings = get_config()
    client = mongo.get_client()

    images = Images(
        client=client,
        settings=settings,
    )
    users = Users(
        client=client,
        settings=settings,
    )

    return Database(
        images=images,
        users=users,
    )
