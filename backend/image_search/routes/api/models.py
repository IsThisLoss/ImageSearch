import typing
import pydantic


# common

class ApiResponse(pydantic.BaseModel):
    status: str
    description: typing.Optional[str] = None


class ObjectInserted(ApiResponse):
    id: typing.Optional[str]


# images

class InputImage(pydantic.BaseModel):
    title: str
    description: str
    media_id: str


class ImagePreview(pydantic.BaseModel):
    medium: str


class ImageLinks(pydantic.BaseModel):
    orig: str
    previews: ImagePreview


class Image(pydantic.BaseModel):
    id: str
    title: str
    description: str
    links: ImageLinks
    ts: typing.Optional[int] = None


class Images(pydantic.BaseModel):
    images: typing.List[Image]


# media

class UploadResponse(pydantic.BaseModel):
    media_id: str


# user

class Token(pydantic.BaseModel):
    access_token: str
    token_type: str
