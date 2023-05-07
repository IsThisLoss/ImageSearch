import functools
import dataclasses

from . import mongo
from .images import Images
from .image_links import ImageLinks
from .users import Users

from ..models.config import get_config


@dataclasses.dataclass
class Database:
    images: Images
    image_links: ImageLinks
    users: Users


@functools.lru_cache()
def get_db():
    settings = get_config()
    client = mongo.get_client()

    images = Images(
        client=client,
        settings=settings,
    )
    image_links = ImageLinks(
        client=client,
        settings=settings,
    )
    users = Users(
        client=client,
        settings=settings,
    )

    return Database(
        images=images,
        image_links=image_links,
        users=users,
    )
