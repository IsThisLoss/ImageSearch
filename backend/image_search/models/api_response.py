from pydantic import BaseModel
from typing import Optional


class ApiResponse(BaseModel):
    status: str
    description: Optional[str] = None


class ObjectInserted(ApiResponse):
    id: Optional[str]
