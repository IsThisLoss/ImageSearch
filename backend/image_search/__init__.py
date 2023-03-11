# import logging


from .routes import app
from .db import mongo


__version__ = "2.0.0"


@app.on_event('startup')
async def init_db():
    # logger = logging.getLogger("uvicorn.error")
    # handler = logging.StreamHandler()
    # handler.setFormatter(
    #    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # )
    # logger.addHandler(handler)
    await mongo.create_indexes()
