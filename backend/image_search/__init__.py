from . import logs

logs.init()

from . import jobs
from .db import mongo
from .routes import app


__version__ = "3.0.0"


@app.on_event('startup')
async def startup():
    jobs.init()
    await mongo.create_indexes()
