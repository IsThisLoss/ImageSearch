from . import clean_image_links
from .. import logs

logger = logs.get_logger()

_jobs = []


def init():
    global _jobs

    _jobs.append(clean_image_links.CleanImageLinks())

    logger.info('Jobs are initialized')
