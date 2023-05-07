import typing
import hashlib

import aioboto3
import functools

from .models import config


class ObjectStorage:
    def __init__(self):
        self._cfg = config.get_config()
        self._bucket = self._cfg.s3_bucket
        self._prefix = self._cfg.media_prefix
    
    def _gen_filename(self, file: typing.IO, extention: str) -> str:
        file_id = hashlib.sha1(file.read()).hexdigest()
        file.seek(0)
        return f'{self._prefix}/{file_id}{extention}'

    async def upload_file(self, file: typing.IO, extention: str) -> str:
        filename = self._gen_filename(file, extention)
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
