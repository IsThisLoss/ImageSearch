# import hashlib
import typing
import uuid

import aioboto3
import functools

from .models import config


class ObjectStorage:
    def __init__(self):
        self._cfg = config.get_config()
        self._bucket = self._cfg.s3_bucket
        self._prefix = self._cfg.media_prefix
    
    def _gen_filename(self, _: typing.IO, extention: str) -> str:
        # file_id = hashlib.sha1(file.read()).hexdigest()
        # file.seek(0)
        file_id = uuid.uuid4().hex
        return f'{self._prefix}/{file_id}{extention}'


    def _content_type(self, extention: str) -> typing.Optional[str]:
        if extention in ('.jpg', '.jpeg'):
            return 'image/jpeg'
        if extention == '.png':
            return 'image/png'
        return None

    async def upload_file(self, file: typing.IO, extention: str) -> str:
        filename = self._gen_filename(file, extention)
        async with aioboto3.Session().client(
            's3',
            endpoint_url=self._cfg.s3_endpoint,
            aws_access_key_id=self._cfg.s3_access_key,
            aws_secret_access_key=self._cfg.s3_secret_key,
        ) as s3:
            params = {
                'Body': file,
                'Bucket': self._bucket,
                'Key': filename,
            }
            content_type = self._content_type(extention)
            if content_type:
                params['ContentType'] = content_type
            await s3.put_object(**params)
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
