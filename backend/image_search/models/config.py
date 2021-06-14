from pydantic import BaseSettings

from functools import lru_cache


class Settings(BaseSettings):
    mongodb_login: str
    mongodb_password: str
    mongodb_host: str = 'localhost'
    mongodb_port: int = 27017
    mongodb_db: str = 'image_search'
    mongodb_image_collection: str = 'images'

    class Config:
        env_file = '.env'


@lru_cache()
def get_config():
    return Settings()
