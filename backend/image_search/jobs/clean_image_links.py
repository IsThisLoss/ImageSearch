import asyncio
import datetime

from .. import logs
from . import job
from .. import db
from .. import object_storage


logger = logs.get_logger()


class CleanImageLinks(job.Job):
    KEEP_LINKS_INTERVAL = datetime.timedelta(hours=1)

    def name(self) -> str:
        return 'clean_image_links'

    def interval(self) -> datetime.timedelta:
        return datetime.timedelta(minutes=30)

    async def do(self):
        database = db.get_db()
        objects = object_storage.get_object_storage()

        now = datetime.datetime.now()
        min_time = int((now - self.KEEP_LINKS_INTERVAL).timestamp())
        links = await database.image_links.find_older_than(min_time)
        ids = []
        for link in links:
            if link.id is None:
                continue
            ids.append(link.id)

            await asyncio.gather(
                objects.remove_key(link.orig),
                objects.remove_key(link.previews.medium),
            )

        await database.image_links.delete_many(ids)
        logger.info('Deleted %s links', len(ids))
