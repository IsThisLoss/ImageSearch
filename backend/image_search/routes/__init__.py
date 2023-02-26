from .api import image, search, media, user
from ..models import config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(image.router)
app.include_router(search.router)
app.include_router(media.router)
app.include_router(user.router)
