from pydantic import BaseModel

__all__ = [
    "BaseSuccessResponse",
]


class BaseSuccessResponse(BaseModel):
    status: str = "success"
    message: str
