from pydantic import BaseModel

from typing import Optional, List


class InputImage(BaseModel):
    title: str
    description: str
    url: str


class Image(InputImage):
    id: str
    cv_text: Optional[str]
    ts: Optional[int]


class Images(BaseModel):
    images: List[Image]
