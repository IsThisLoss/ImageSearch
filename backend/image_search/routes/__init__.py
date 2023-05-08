

from .api import image, media, user

from fastapi import FastAPI


app = FastAPI()
app.include_router(image.router)
app.include_router(media.router)
app.include_router(user.router)
