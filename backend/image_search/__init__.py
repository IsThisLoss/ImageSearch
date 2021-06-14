from .routes import app
from .db import mongo


@app.on_event('startup')
async def init_db():
    await mongo.create_indexes()
