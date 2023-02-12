from fastapi import APIRouter, File, UploadFile, Depends

from ...models import media, config
from ... import object_storage

from . import user

router = APIRouter(prefix='/api')


@router.post('/media', response_model=media.UploadResponse)
async def get_images(file: UploadFile = File(...), _ = Depends(user.get_current_user)):
    storage = object_storage.get_object_storage()
    url = await storage.upload_file(
        file.file._file,
        file.content_type,
    )
    cfg = config.get_config()
    url = f'{cfg.s3_endpoint}/{cfg.s3_bucket}{url}'
    return media.UploadResponse(url=url)
