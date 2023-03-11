from fastapi import APIRouter, File, UploadFile, Depends

from ...models import media
from ...object_storage import ObjectStorage, get_object_storage

from . import user


router = APIRouter(prefix='/api')


@router.post('/media', response_model=media.UploadResponse)
async def upload_media(
    file: UploadFile = File(...),
    object_storage: ObjectStorage = Depends(get_object_storage),
    _ = Depends(user.get_current_user),
):
    url = await object_storage.upload_file(
        file.file._file,
        file.content_type,
    )
    return media.UploadResponse(url=url)
