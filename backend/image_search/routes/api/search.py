from fastapi import APIRouter

from ...models.image_storage import get_image_storage
from ...models.image import Images


router = APIRouter(prefix='/api')


@router.get('/search/image', response_model=Images)
async def get_search_image(text: str):
    image_storage = get_image_storage()
    images = await image_storage.search(text)
    return Images(images=images)
