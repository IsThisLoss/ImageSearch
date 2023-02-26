import aioboto3
import functools
# import logging
import uuid

from .models import config


class ObjectStorage:
    def __init__(self):
        self._cfg = config.get_config()
        self._bucket = self._cfg.s3_bucket
        self._prefix = self._cfg.media_prefix
    
    def _gen_filename(self, content_type: str) -> str:
        file_id = str(uuid.uuid4())
        ext = ''
        if content_type == 'image/jpeg':
            ext = '.jpg'
        elif content_type == 'image/png':
            ext = '.png'
        return f'{self._prefix}/{file_id}{ext}'

    async def upload_file(self, file, content_type) -> str:
        filename = self._gen_filename(content_type)
        async with aioboto3.Session().client(
            's3',
            endpoint_url=self._cfg.s3_endpoint,
            aws_access_key_id=self._cfg.s3_access_key,
            aws_secret_access_key=self._cfg.s3_secret_key,
        ) as s3:
            await s3.put_object(
                Body=file,
                Bucket=self._bucket,
                Key=filename,
            )
        return filename

    async def remove_key(self, key: str):
        # logger = logging.getLogger("uvicorn.error")
        # logger.info('Going to remove %s', key)
        async with aioboto3.Session().client(
            's3',
            endpoint_url=self._cfg.s3_endpoint,
            aws_access_key_id=self._cfg.s3_access_key,
            aws_secret_access_key=self._cfg.s3_secret_key,
        ) as s3:
            await s3.delete_object(
                Bucket=self._bucket,
                Key=key,
            )


@functools.lru_cache()
def get_object_storage():
    return ObjectStorage()
