import dataclasses

from pydantic import BaseModel


@dataclasses.dataclass
class User:
    username: str


class Token(BaseModel):
    access_token: str
    token_type: str
