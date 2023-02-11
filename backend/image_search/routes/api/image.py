from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from ...models.image_storage import get_image_storage
from ...models.image import InputImage, Image, Images
from ...models.api_response import ObjectInserted, ApiResponse
from .user import get_current_user


router = APIRouter(prefix='/api')


@router.get('/image', response_model=Images)
async def get_images(user = Depends(get_current_user)):
    image_storage = get_image_storage()
    images = await image_storage.get_all(user.username)
    return Images(images=images)


@router.get('/image/{id}', response_model=Image)
async def get_image(id: str, user = Depends(get_current_user)):
    image_storage = get_image_storage()
    image = await image_storage.get(user.username, id)
    if not image:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
        )
    return image


@router.post('/image', response_model=ObjectInserted)
async def post_image(image: InputImage, user = Depends(get_current_user)):
    image_storage = get_image_storage()
    inserted_id = await image_storage.put(user.username, image)
    result = ObjectInserted(status='OK', id=inserted_id)
    return result


@router.put('/image/{id}', response_model=ObjectInserted)
async def put_image(id: str, image: InputImage, user = Depends(get_current_user)):
    image_storage = get_image_storage()
    status = await image_storage.update(user, id, image)
    if status:
        return ObjectInserted(status='OK', id=id)
    return JSONResponse(status_code=404, content=ObjectInserted(status='NOT FOUND', id=id).dict())


@router.delete('/image/{id}', response_model=ApiResponse)
async def delete_image(id: str, user = Depends(get_current_user)):
    image_storage = get_image_storage()
    await image_storage.delete(user.username, id)
    result = ApiResponse(status='OK')
    return result
