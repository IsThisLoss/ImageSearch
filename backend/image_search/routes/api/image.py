import typing

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from . import models
from ... import db
from ... import object_storage
from ...models import config
from .user import User, get_current_user


router = APIRouter(prefix='/api')


def to_models(
    image: db.images.Image,
    image_domain: str,
) -> models.Image:
    if image.id is None:
        raise ValueError("Image id must be present")
    return models.Image(
        id=image.id,
        title=image.title,
        description=image.description,
        links=models.ImageLinks(
            orig=image_domain + image.links.orig,
            previews=models.ImagePreview(
                medium=image_domain + image.links.previews.medium,
            ),
        ),
        ts=image.ts,
    )


@router.get('/image', response_model=models.Images)
async def get_images(
    text: typing.Optional[str] = None,
    offset: int = 0,
    limit: int = 100,
    user: User = Depends(get_current_user),
    database: db.Database = Depends(db.get_db),
):
    images = await database.images.find(
        user.username,
        text,
        offset,
        limit,
    )

    image_domain = config.get_config().image_domain
    result = []
    for image in images:
        result.append(to_models(image,image_domain))
    return models.Images(images=result)


@router.get('/image/{id}', response_model=models.Image)
async def get_image(
    id: str,
    user: User = Depends(get_current_user),
    database: db.Database = Depends(db.get_db),
):
    image = await database.images.get(user.username, id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
    image_domain = config.get_config().image_domain
    return to_models(image, image_domain)


@router.post('/image', response_model=models.ObjectInserted)
async def post_image(
    input_image: models.InputImage,
    user: User = Depends(get_current_user),
    database: db.Database = Depends(db.get_db),
):
    image_links = await database.image_links.get(input_image.media_id)
    if not image_links:
        body = models.ApiResponse(
            status='MEDIA_NOT_FOUND',
            description=f'No such media_id: {input_image.media_id}',
        ).dict()
        return JSONResponse(
            status_code=400,
            content=body,
        )

    image = db.images.Image(
        id=None,
        username=user.username,
        title=input_image.title,
        description=input_image.description,
        links=db.images.ImageLinks(
            orig=image_links.orig,
            previews=db.images.ImagePreview(
                medium=image_links.previews.medium,
            ),
        ),
    )

    inserted_id = await database.images.put(user.username, image)
    result = models.ObjectInserted(status='OK', id=inserted_id)
    await database.image_links.delete(input_image.media_id)
    return result


@router.delete('/image/{id}', response_model=models.ApiResponse)
async def delete_image(
    id: str,
    user: User = Depends(get_current_user),
    database: db.Database = Depends(db.get_db),
    object_storage: object_storage.ObjectStorage = Depends(object_storage.get_object_storage),
):
    result = models.ApiResponse(status='OK')

    image = await database.images.get(user.username, id)
    if not image:
        return result

    await database.images.delete(user.username, id)
    await object_storage.remove_key(image.links.orig)
    await object_storage.remove_key(image.links.previews.medium)
    return result
