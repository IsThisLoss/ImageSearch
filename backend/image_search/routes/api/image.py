from fastapi import APIRouter
from fastapi.responses import JSONResponse

from ...models.image_storage import get_image_storage
from ...models.image import InputImage, Image, Images
from ...models.api_response import ObjectInserted, ApiResponse


router = APIRouter(prefix='/api')


@router.get('/image', response_model=Images)
async def get_images():
    image_storage = get_image_storage()
    images = await image_storage.get_all()
    return Images(images=images)


@router.get('/image/{id}', response_model=Image)
async def get_image(id: str):
    image_storage = get_image_storage()
    image = await image_storage.get(id)
    return image


@router.post('/image', response_model=ObjectInserted)
async def post_image(image: InputImage):
    image_storage = get_image_storage()
    inserted_id = await image_storage.put(image)
    result = ObjectInserted(status='OK', id=inserted_id)
    return result


@router.put('/image/{id}', response_model=ObjectInserted)
async def put_image(id: str, image: InputImage):
    image_storage = get_image_storage()
    status = await image_storage.update(id, image)
    if status:
        return ObjectInserted(status='OK', id=id)
    return JSONResponse(status_code=404, content=ObjectInserted(status='NOT FOUND', id=id).dict())


@router.delete('/image/{id}', response_model=ApiResponse)
async def delete_image(id: str):
    image_storage = get_image_storage()
    await image_storage.delete(id)
    result = ApiResponse(status='OK')
    return result
