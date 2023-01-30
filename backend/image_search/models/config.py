from pydantic import BaseSettings

from functools import lru_cache


class Settings(BaseSettings):
    mongodb_login: str = 'image_search'
    mongodb_password: str = 'image_search_password'
    mongodb_host: str = 'localhost'
    mongodb_port: int = 27017
    mongodb_db: str = 'image_search'
    mongodb_image_collection: str = 'images'

    web_origin: str = ""

    s3_endpoint: str = 'http://localhost:9000'
    s3_access_key: str = 'image_search'
    s3_secret_key: str = 'image_search_password'
    s3_bucket: str = 'image-search'

    media_prefix: str = '/media'

    class Config:
        env_file = '.env'


@lru_cache()
def get_config():
    return Settings()
