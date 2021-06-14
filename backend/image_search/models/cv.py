import pytesseract
from PIL import Image
import io
import aiohttp

import sys


async def get_image_from_url(url: str) -> Image:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            raw_image = await response.read()
    return Image.open(io.BytesIO(raw_image))


def get_text_from_image(image: Image) -> str:
    cv_text = pytesseract.image_to_string(image, lang='eng+rus')
    return " ".join(cv_text.replace('\n', ' ').split())


async def get_text_from_image_url(url: str) -> str:
    try:
        image = await get_image_from_url(url)
        return get_text_from_image(image)
    except Exception as e:
        # TODO add logger
        sys.stderr.write(str(e))
        return ""
