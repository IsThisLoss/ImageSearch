import typing

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from ...db import Database, get_db
from ...models.api_response import ObjectInserted, ApiResponse
from ...models.image import InputImage, Image, Images
from ...object_storage import ObjectStorage, get_object_storage
from .user import User, get_current_user


router = APIRouter(prefix='/api')


@router.get('/image', response_model=Images)
async def get_images(
    text: typing.Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
    user: User = Depends(get_current_user),
    db: Database = Depends(get_db),
):
    images = await db.images.find(
        user.username,
        text,
        offset,
        limit,
    )
    return Images(images=images)


@router.get('/image/{id}', response_model=Image)
async def get_image(
    id: str,
    user: User = Depends(get_current_user),
    db: Database = Depends(get_db),
):
    image = await db.images.get(user.username, id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return image


@router.post('/image', response_model=ObjectInserted)
async def post_image(
    image: InputImage,
    user: User = Depends(get_current_user),
    db: Database = Depends(get_db),
):
    inserted_id = await db.images.put(user.username, image)
    result = ObjectInserted(status='OK', id=inserted_id)
    return result


@router.put('/image/{id}', response_model=ObjectInserted)
async def put_image(
    id: str,
    image: InputImage,
    user: User = Depends(get_current_user),
    db: Database = Depends(get_db),
):
    status = await db.images.update(user.username, id, image)
    if status:
        return ObjectInserted(status='OK', id=id)
    body = ObjectInserted(status='NOT FOUND', id=id).dict()
    return JSONResponse(
        status_code=404,
        content=body,
    )


@router.delete('/image/{id}', response_model=ApiResponse)
async def delete_image(
    id: str,
    user: User = Depends(get_current_user),
    db: Database = Depends(get_db),
    object_storage: ObjectStorage = Depends(get_object_storage),
):
    result = ApiResponse(status='OK')

    image = await db.images.get(user.username, id)
    if not image:
        return result

    await db.images.delete(user.username, id)
    await object_storage.remove_key(image.url)
    return result
