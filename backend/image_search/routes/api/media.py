from fastapi import APIRouter, File, UploadFile

from ...models import media
from ... import object_storage

router = APIRouter(prefix='/api')


@router.post('/media', response_model=media.UploadResponse)
async def get_images(file: UploadFile = File(...)):
    storage = object_storage.get_object_storage()
    url = await storage.upload_file(
        file.file._file,
        file.content_type,
    )
    return media.UploadResponse(url=url)
