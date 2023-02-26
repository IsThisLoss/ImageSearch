from .routes import app
from .db import mongo


__version__ = "1.0.4"


@app.on_event('startup')
async def init_db():
    await mongo.create_indexes()
