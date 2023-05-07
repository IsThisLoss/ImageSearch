import io

from fastapi import APIRouter, File, UploadFile, Depends
import imutils
import numpy
import cv2

from . import models
from . import user
from ... import db
from ... import object_storage


router = APIRouter(prefix='/api')


MEDIUM_HEIGHT = 720
PREVIEW_EXTENTION = '.jpg'


def get_file_extention(content_type, default='') -> str:
    if content_type == 'image/jpeg':
        return '.jpg'
    elif content_type == 'image/png':
        return '.png'
    return default


def create_preview(image_buf: bytes) -> bytes:
    matrix = numpy.frombuffer(image_buf, dtype=numpy.uint8)
    cv_img = cv2.imdecode(matrix, cv2.IMREAD_COLOR)
    cv_preview = imutils.resize(
        cv_img,
        height=MEDIUM_HEIGHT,
    )
    result = cv2.imencode(PREVIEW_EXTENTION, cv_preview)[1].tostring()
    return result


@router.post('/media', response_model=models.UploadResponse)
async def upload_media(
    file: UploadFile = File(...),
    database: db.Database = Depends(db.get_db),
    object_storage: object_storage.ObjectStorage = Depends(object_storage.get_object_storage),
    _ = Depends(user.get_current_user),
):
    image_buf: bytes = file.file.read()

    orig = await object_storage.upload_file(
        file=io.BytesIO(image_buf),
        extention=get_file_extention(file.content_type),
    )

    preview_buf = create_preview(image_buf)
    medium = await object_storage.upload_file(
        file=io.BytesIO(preview_buf),
        extention=PREVIEW_EXTENTION,
    )

    image_link = db.image_links.ImageLink(
        id=None,
        orig=orig,
        previews=db.image_links.ImagePreview(
            medium=medium,
        ),
    )
    media_id = await database.image_links.put(image_link)

    return models.UploadResponse(media_id=media_id)
