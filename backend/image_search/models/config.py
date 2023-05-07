import functools
import pydantic


class Settings(pydantic.BaseSettings):
    mongodb_login: str = 'image_search'
    mongodb_password: str = 'image_search_password'
    mongodb_host: str = 'localhost'
    mongodb_port: int = 27017
    mongodb_db: str = 'image_search'

    s3_endpoint: str = 'http://localhost:9000'
    s3_access_key: str = 'image_search'
    s3_secret_key: str = 'image_search_password'
    s3_bucket: str = 'image-search'

    # prefix for key in bucket
    media_prefix: str = '/media'

    # prefix for bucket keys
    #when replying to frontend
    image_domain: str = ''

    secret: str = 'secret'
    access_token_expire_minutes: int = 120

    class Config:
        env_file = '.env'


@functools.lru_cache()
def get_config():
    return Settings()
