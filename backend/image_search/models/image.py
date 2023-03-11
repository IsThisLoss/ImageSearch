import typing

from pydantic import BaseModel


class InputImage(BaseModel):
    title: str
    description: str
    url: str


class Image(InputImage):
    id: str
    cv_text: typing.Optional[str]
    ts: typing.Optional[int]


class Images(BaseModel):
    images: typing.List[Image]
