import abc
import asyncio
import datetime

from .. import logs


logger = logs.get_logger()


class Job:
    def __init__(self):
        self._task = asyncio.create_task(
            self.run(),
            name=self.name(),
        )

    @abc.abstractmethod
    def name(self) -> str:
        raise NotImplemented

    @abc.abstractmethod
    def interval(self) -> datetime.timedelta:
        raise NotImplemented

    @abc.abstractmethod
    async def do():
        raise NotImplemented

    async def run(self):
        name = self.name()
        delta = self.interval()
        while True:
            logger.info('Start job %s', name)
            try:
                await self.do()
            except Exception as _:
                logger.exception('Faild to run %s', name)
            else:
                logger.info('Finish job %s', name)
            await asyncio.sleep(delta.total_seconds())
