from fastapi import APIRouter, Depends

from ...models.image_storage import get_image_storage
from ...models.image import Images
from .user import get_current_user

router = APIRouter(prefix='/api')


@router.get('/search/image', response_model=Images)
async def get_search_image(text: str, user = Depends(get_current_user)):
    image_storage = get_image_storage()
    images = await image_storage.search(user.username, text)
    return Images(images=images)
