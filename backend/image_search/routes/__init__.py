from .api import image, search

from fastapi import FastAPI


app = FastAPI()
app.include_router(image.router)
app.include_router(search.router)
