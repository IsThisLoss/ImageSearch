from .api import image, search
from ..models import config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


origins = (
    config.get_config().web_origin,
)

app = FastAPI()
app.include_router(image.router)
app.include_router(search.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
